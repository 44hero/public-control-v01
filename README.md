# public-control-v01
特定権限者のみへの 公開の権限 をコントロールしています -v01-

## 実行サンプル

例えば、yoRigGenericToolGroup -5.5- <py 3.7.7, ui:PySide2 5.15.2> についてです。

[yoRigGenericToolGroup 動作動画](https://i.gyazo.com/9c1172e56e9fc4eca9ea4036239624ec.mp4)

<a href="https://gyazo.com/9c1172e56e9fc4eca9ea4036239624ec"><video width="1120" autoplay muted loop playsinline controls><source src="https://i.gyazo.com/9c1172e56e9fc4eca9ea4036239624ec.mp4" type="video/mp4"/></video></a>

<a href="https://gyazo.com/9c1172e56e9fc4eca9ea4036239624ec"><img src="https://i.gyazo.com/9c1172e56e9fc4eca9ea4036239624ec.gif" alt="Image from Gyazo" width="1120"/></a>

<details>
  <summary>例えば、yoRigGenericToolGroup -5.5- <py 3.7.7, ui:PySide2 5.15.2> についてです。</summary>
  
note: 当コード記述時の環境

    - Maya2022 python3系
    - Python version: 3.7.7
    - PyMel version: 1.2.0
    - PySide2 version: 5.15.2

zipダウンロードし解凍ののち、YO_utilityToolsフォルダ 毎、
ユーザー側での、所定のMaya のスクリプト パス直下に、コピーのうえ、
例えば、maya script editor python タブ で、以下をタイピングのうえ、実行してください。

```python
from imp import reload
import YO_utilityTools.rigGenericToolGroup.yoRigGenericToolGroup_main
reload(YO_utilityTools.rigGenericToolGroup.yoRigGenericToolGroup_main)
from YO_utilityTools.rigGenericToolGroup import yoRigGenericToolGroup_main
yoRigGenericToolGroup_main.main()
```

### ●開発の経緯・ストーリー
ユーザーの Mayaスクリプトパスへの、自前パッケージごとのコピーで、自前パッケージを、エラー無く提供ができる仕組みを確立してみたかったのです。

こだわったところは、

1. MVC設計を意識した ツール開発
1. 最終目標である、PySide2 UI仕様 でのツール開発
1. クラス継承と名前空間の理解
1. シングルトンの理解

です。

### ●使用した技術

- フロント・クライアント技術


- サーバーサイド技術

    Python 3系, PySide2, PyMel, Maya command

- DB・ミドルウェア技術


- インフラ/その他専門技術


### ●使用した技術の選定理由
きっかけは、
(株)ポリゴンピクチュアズ における、高度な技術を目の当たりにしてからです。
自身が一人だちするに当たり、自身の不足箇所が非常に明らかになりました。
そこで、自身のスキルアップに価値を見出しました。
自身をスキルをアップしない事には、ただでさえ作業に多くの時間を費やすリグ作業において、自身が疲弊するだけであると。

大別して、

■ Maya上で動作する、リグのスキルアップ

■ そのリグ作業を支援するツール開発をするにあたり、pythonプログラムを用いたツール開発のスキルアップ

以上を大命題にすえます。


■活かせる経験・知識・技術
2024/5/25 現在
最新の、スキルを以下に詳らかに致します。

■■■ pythonプログラミング Maya用ツール開発 のスキル ■■■
- python パッケージ と モジュール のノウハウ
- 名前空間 について
- シングルトン モジュール について
- MVCモデル を意識した システム開発設計方針 について
- クラス継承 について
- Maya上で動作する様々なUI の理解 について(現在 Maya2022 Python3系)
    - Maya command UI
    - Maya PyMel UI
    - Maya PySide2 UI
- UI 入力データ の管理方法 について

■■■ Maya上で動作するリグ のスキルアップ ■■■
- アニメータに優しい軽量な リグ動作 の考察と実現 のノウハウ
- 標準コンストレインを用いずMatrixノードを多用したリグの実現 のノウハウ
- 作業分担 の実現 のノウハウ

</details>

<details>
  <summary>YO_utilityTools パッケージ tree 構成</summary>
  
```shell
C:.
│  yoCustomScriptEditor2StandAlone.py
│  yoIsHistoricallyInteresting.py
│  YO_constraintToGeometry2.py
│  YO_jointDrawStyle_change.py
│  YO_jointRadiusSlider.py
│  YO_nodeCreateToWorldSpace.py
│  YO_parentConstraintByMatrix5.py
│  YO_parentConstraintByMatrix62.py
│  __init__.py
│
├─createClusterAndRenameTool
│      config.py
│      YO_createClusterAndRename6_Ctlr.py
│      YO_createClusterAndRename6_main.py
│      YO_createClusterAndRename6_Modl.py
│      YO_createClusterAndRename6_View.py
│      __init__.py
│
├─createSpaceNode
│      config.py
│      YO_createSpaceNode3_Ctlr.py
│      YO_createSpaceNode3_main.py
│      YO_createSpaceNode3_Modl.py
│      YO_createSpaceNode3_View.py
│      __init__.py
│
├─createSpIkAndRenameTool
│      config.py
│      YO_createSpIkAndRename3_Ctlr.py
│      YO_createSpIkAndRename3_main.py
│      YO_createSpIkAndRename3_Modl.py
│      YO_createSpIkAndRename3_View.py
│      __init__.py
│
├─lib
│      commonCheckCurve.py
│      commonCheckJoint.py
│      commonCheckMesh.py
│      commonCheckSelection.py
│      commonCheckShape.py
│      commonCheckSkinCluster.py
│      commonCheckSurface.py
│      commonInverseScaleConnection_AtoB_2.py
│      message.py
│      message_warning.py
│      yoGetAttributeFromModule.py
│      YO_logger2.py
│      YO_optionVar.py
│      YO_printLoadedModules.py
│      YO_uuID.py
│      YO_validate.py
│      __init__.py
│
├─orientConstraintByMatrix
│      config.py
│      YO_orientConstraintByMatrix1_Ctlr.py
│      YO_orientConstraintByMatrix1_main.py
│      YO_orientConstraintByMatrix1_Modl.py
│      YO_orientConstraintByMatrix1_View.py
│      __init__.py
│
├─pointConstraintByMatrix
│      config.py
│      YO_pointConstraintByMatrix1_Ctlr.py
│      YO_pointConstraintByMatrix1_main.py
│      YO_pointConstraintByMatrix1_Modl.py
│      YO_pointConstraintByMatrix1_View.py
│      __init__.py
│
├─renameTool
│      config.py
│      YO_renameTool5_Ctlr.py
│      YO_renameTool5_main.py
│      YO_renameTool5_Modl.py
│      YO_renameTool5_View.py
│      __init__.py
│
├─rigGenericToolGroup
│  │  config.py
│  │  yoRigGenericToolGroup_Ctlr.py
│  │  yoRigGenericToolGroup_main.py
│  │  yoRigGenericToolGroup_Modl.py
│  │  yoRigGenericToolGroup_View.py
│  │  __init__.py
│
├─scaleConstraintByMatrix
│      config.py
│      YO_scaleConstraintByMatrix1_Ctlr.py
│      YO_scaleConstraintByMatrix1_main.py
│      YO_scaleConstraintByMatrix1_Modl.py
│      YO_scaleConstraintByMatrix1_View.py
│      __init__.py
│
├─shearConstraintByMatrix
│      config.py
│      YO_shearConstraintByMatrix1_Ctlr.py
│      YO_shearConstraintByMatrix1_main.py
│      YO_shearConstraintByMatrix1_Modl.py
│      YO_shearConstraintByMatrix1_View.py
│      __init__.py
│
├─skinWeightsExpImpTool
│  │  config.py
│  │  yoSkinWeightsExpImpTool_Ctlr.py
│  │  yoSkinWeightsExpImpTool_main.py
│  │  yoSkinWeightsExpImpTool_Modl.py
│  │  yoSkinWeightsExpImpTool_View.py
│  │  __init__.py
│  │
│
├─TemplateForPySide2
│  │  Container.py
│  │  CustomScriptEditor.py
│  │  CustomScriptEditor2.py
│  │  CustomScriptEditor2SPIModule.py
│  │  MyTabWidget.py
│  │  pyside2IniFileSetting.py
│  │  qt.py
│  │  __init__.py
│  │
│  ├─type1
│  │      config.py
│  │      templateForPySide2_type1_Ctlr.py
│  │      templateForPySide2_type1_main.py
│  │      templateForPySide2_type1_Modl.py
│  │      templateForPySide2_type1_View.py
│  │      __init__.py
│  │
│  └─type2
│          config.py
│          templateForPySide2_type2_Ctlr.py
│          templateForPySide2_type2_main.py
│          templateForPySide2_type2_Modl.py
│          templateForPySide2_type2_View.py
│          __init__.py

      
```
</details>


