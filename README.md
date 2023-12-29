# readme

## 编译链相关

### .launch结构

相关内容写在 test.launch 中

### .cpp结构

继承自控制基类 `/opt/ros/noetic/include/controller_interface/controller_base.h`
在代码中重构相关虚函数即可

- `ControllerBase`
  - 用于重载的虚函数
    1. `starting`
    2. `update`
    3. `stopping`
    4. `waiting`
    5. `aborting`
    6. `initRequest`
  - 用于检查的标志位
    1. `isInitialized`
    2. `isRunning`
    3. `isStopped`
    4. `isWaiting`
    5. `isAborted`
  - 紧急状态请求
    1. `updateRequest` `state_ = RUNNING`
    2. `startRequest` `state_ = CONSTRUCTED`
    3. `stopRequest` `state_ = CONSTRUCTED`
    4. `waitRequest` `state_ = CONSTRUCTED`
    5. `abortRequest` `state_ = CONSTRUCTED`
  - 状态
    1. `CONSTRUCTED`
    2. `INITIALIZED`
    3. `RUNNING`
    4. `STOPPED`
    5. `WAITING`
    6. `ABORTED`
- `MultiInterfaceController`
  - 需要重载的虚函数
    - `init`

但是仍然没有找到函数入口和辨别标志。

## 控制代码相关

### franka::RobotState

里面的姿态怎么都是四元数阿……

```cpp
enum class RobotMode {
  kOther,
  kIdle,
  kMove,
  kGuiding,
  kReflex,
  kUserStopped,
  kAutomaticErrorRecovery
};
```

变量的前缀后缀含义

- 前缀
  1. `O_` o-框架基础位姿
  2. `F_` 法兰框架位姿
  3. `NE_` 末端执行器框架位姿
  4. `EE_`
  5. `K` 刚度框架位姿
  6. `I_` 惯性张量
  7. `m_` 质量
  8. `x_` 位置
  9. `tau_` 力矩
  10. `q_` joint position 关节
  11. `dq_` joint velocity 关节速度
  12. `ddq_` joint velocity 关节加速度
  13. `theta_` Motor position
  14. `dtheta_` Motor velocity
- 中缀
  1. `_T_` to
  2. `_hat_` $\hat{}$
  3. `_ext_` $_{\text{ext}}$
- 后缀
  1. `_d` desired 计划值
  2. `_c` Commanded 控制值
  3. `_J` joint 关节
  4. `_load` 负载
  5. `_Cload` 负载质心
  6. `_Cee` 质心
  7. `_total` 总和

### api 相关

1. 句柄类
   1. `state_handle_` 机械臂状态句柄
   2. 获取机械臂状态，返回值为 `franka::RobotState` ,`franka::RobotState ${STATE_NAME} = state_handle_->getRobotState();`
   3. `model_handle_` 机械臂模型句柄
   4. 获取当前的 `Jacobian` 矩阵，返回值为 `std::array<double, 42>`,`${JACOBIAN_ARRAY_NAME} = model_handle_->getZeroJacobian(franka::Frame::kEndEffector);`
   5. 获取当前的科氏向量 ，返回值为 `std::array<double, 7>`,`${CORIOLIS_ARRAY_NAME} = model_handle_->getCoriolis()`
   6. `joint_handles_` 机械臂关节句柄
   7. 将计算好的关节力矩发送给机械臂，`joint_handles_[i]->setCommand(tau_d(i));`
2. `franka::RobotState` 机械臂状态
   1. 获取当前关节角度,返回值为 `std::array<double, 7>`,`${JOINT_ARRAY_NAME} = robot_state.q.data();`
3. 变换类
   1. `Eigen::Affine3d ${Transform_NAME}`
      1. 需要用 4x4 的矩阵初始化
      2. 对于每一个姿态(`O_T_EE`)有其对应的仿射变换矩阵，一个例子写为 `Eigen::Affine3d ${Transform_NAME}(Eigen::Matrix4d::Map(${STATE_NAME}.O_T_EE.data()));`
      3. 获取三维位置，返回值为 `Eigen::Vector3d`,`${POSITION_NAME} = ${Transform_NAME}.translation();`
      4. 获取四元数姿态，返回值为 `Eigen::Quaterniond`,`${ORIENTATION_NAME} = Eigen::Quaterniond(${Transform_NAME}.rotation());`

### cartesian_impedance_example_controller

笛卡尔 阻抗控制器

- `src/franka_ros/franka_example_controllers/include/franka_example_controllers/pseudo_inversion.h`
  - 在头文件中定义了通过SVD分解求伪逆的函数
- `src/franka_ros/franka_example_controllers/include/franka_example_controllers/cartesian_impedance_example_controller.h`
  - 继承了控制器基类，重构了相关函数
    1. `init()`：初始化函数，用于初始化控制器
    2. `starting()`：启动函数，用于启动控制器
    3. `update()`：更新函数，用于更新控制器
  - 创建句柄参数，可以通过调用句柄api获得相关参数及变量
    1. `state_handle_` 机械臂状态句柄
       1. 获取机械臂状态，返回值为 `franka::RobotState` ,`franka::RobotState ${STATE_NAME} = state_handle_->getRobotState();`
    2. `model_handle_` 机械臂模型句柄
       1. 获取当前的 `Jacobian` 矩阵，返回值为 `std::array<double, 42>`,`${JACOBIAN_ARRAY_NAME} = model_handle_->getZeroJacobian(franka::Frame::kEndEffector);`
       2. 获取当前的科氏向量 ，返回值为 `std::array<double, 7>`,`${CORIOLIS_ARRAY_NAME} = model_handle_->getCoriolis()`
    3. `joint_handles_` 机械臂关节句柄
       1. 将计算好的关节力矩发送给机械臂，`joint_handles_[i]->setCommand(tau_d(i));`
  - 创建过程中的相关变量及参数
    1. `Matrix<double, 6, 6> cartesian_stiffness_` 机械臂的刚度矩阵
    2. `Matrix<double, 6, 6> cartesian_stiffness_target_` 机械臂的目标刚度矩阵
    3. `Matrix<double, 6, 6> cartesian_damping_` 机械臂的阻尼矩阵
    4. `Matrix<double, 6, 6> cartesian_damping_target_` 机械臂的目标阻尼矩阵
    5. `Matrix<double, 7, 1> q_d_nullspace_` 零空间
    6. `Vector3d position_d_` 位置
    7. `Quaterniond orientation_d_;` 姿态,四元数格式
    8. `std::mutex position_and_orientation_d_target_mutex_` 互斥锁,不知道干啥用
    9. `Vector3d position_d_target_;` 目标位置
    10. `Quaterniond orientation_d_target_;` 目标姿态
- `src/franka_ros/franka_example_controllers/src/cartesian_impedance_example_controller.cpp`
  - `init()`
  - `starting()`
    - 初始化姿态和目标姿态，从RobotState中获取平移和旋转分量
  - `update()`
