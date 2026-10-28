# PAI Final Project: AI Pick and Place

Physical AI応用1講座の最終課題です。

## 1. 概要

PC部品の再利用判定とロボットアームによる
自動搬送を組み合わせたシミュレーションです。

模擬検査データをもとにAIが再利用可否を判定し、
結果に応じてロボットアームの搬送を実行・停止します。

## 2. 使用技術

- Ubuntu 22.04
- ROS 2 Humble
- Gazebo Fortress
- UR5eロボットアーム
- Robotiqグリッパー
- Python / scikit-learn

## 3. AIの仕組み

12件の模擬検査文章を教師データとして使用します。

- 特徴量抽出：TF-IDF（文字2〜3-gram）
- 分類モデル：Multinomial Naive Bayes
- 出力：reuse（再利用可能）/ hold（要確認）

reuseの場合はPick & Placeを実行し、
holdの場合は搬送を実行しません。

## 4. 実行方法

Ubuntu 22.04、ROS 2 Humble、
Gazebo Fortressの環境を前提とします。

必要なROS 2パッケージとscikit-learnを
インストールした後、以下を実行します。

### ビルド

```bash
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
```

### Gazeboの起動

```bash
ros2 launch ur5e_gripper_gazebo ur5e_robotiq_gazebo.launch.py
```

### AI判定とロボット搬送

別ターミナルでROS 2環境を読み込みます。

```bash
source /opt/ros/humble/setup.bash
source install/setup.bash
python3 ai_pick_place.py "電源が入らない 破損あり" --execute
python3 ai_pick_place.py "起動正常 動作良好 破損なし" --execute
```

## 5. 実装結果

- 要確認：AIが搬送不要と判定し、ロボットは停止
- 再利用可能：AIが搬送を許可し、Pick & Placeを実行

UR5eロボットアームが立方体を把持し、
所定位置に運搬・配置する動作を確認しました。

## 6. 工夫した点と制約

既存のPick & Placeサンプルに対し、
検査結果の機械学習による分類と
搬送実行可否の判断機能を追加しました。

今回のAIは入力文章を分類するものであり、
画像認識や把持位置の補正は行っていません。
また、模擬データを使用した学習のため、
実際のPC部品の品質判定には使用できません。

## 7. 参考・出典

ロボットアームのシミュレーションには、
以下の公開サンプルを利用しました。

https://github.com/Farhan3376/Pick-and-Place-Robotic-Arm-using-Ros2-

UR5eとRobotiqグリッパーのモデルおよび
Pick & Placeの制御コードを利用しています。

ROS 2 Humbleのインストール済みパッケージとの
互換性のため、Xacroの引数名を一部修正しました。

元コードの著作権・ライセンスについては
上記の公開元を参照してください。
