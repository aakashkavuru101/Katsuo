# katsuo 🐟

[![Tests](https://github.com/AllBlue-inc/Katsuo/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/AllBlue-inc/Katsuo/actions/workflows/test.yml)
![Live E2E](https://img.shields.io/badge/live%20E2E-Claude%20Code%20%2B%20Codex%20passed-2ea44f)
![Version](https://img.shields.io/badge/version-0.1.0-2563eb)
![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-d97757)
![Codex](https://img.shields.io/badge/Codex-plugin-111827)

[English](README.md) | **日本語**

好奇心旺盛な、あなたのAI開発パートナー。
かつお節の出汁のように、ひとつの素材から豊かな価値を引き出します。

```text
/katsuo メールによるパスワードリセットを追加
```

仕様策定 → テスト駆動開発 → 独立レビュー → Pull Request。これだけです。

## Katsuoの考え方

Katsuoは好奇心旺盛な魚です。行動する前に必要な情報を集め、あなたの代わりではなく、あなたと一緒に判断します。判断にあなたの意思が必要なときは質問します。あなたが迷っているときは選択肢を調べ、難しい言葉を使わずにおすすめを説明します。

あなたとKatsuoはチームです。プライバシーとセキュリティを最優先にします。変更が小さいか大きいかを一緒に判断し、全体を一度に完成させようとせず、役に立つ機能を一つずつ完成させます。すべての変更を分かりやすい手順で進め、プロジェクトに合わせて調整し、きちんと動く最小限の形に保ちます。専門知識がなくても、誰でも簡単に使えることを大切にしています。

## 原則

- **好奇心:** 判断する前にプロジェクトを確認し、根拠を集めます。
- **一緒に判断:** 結果やリスクが変わる判断には、あなたの意思を反映します。
- **分かりやすく:** 初めての内容も、やさしい言葉で説明します。
- **プライバシーとセキュリティ:** データ、秘密情報、アクセス権、ユーザーの主導権を標準で守ります。
- **明確な手順:** 仕様 → 実装 → レビュー → PRの流れで進めます。
- **適切な規模:** 変更が小さいか大きいか、その理由と最初に取り組む範囲を説明し、あなたと合意します。
- **機能単位:** 一つの役に立つ機能を完成させてから、次へ進みます。
- **最小限で高機能:** 必要なことを満たす、最も小さな解決策を作ります。
- **高い適応力:** プロジェクトのツール、環境、ユーザーの経験に合わせます。

## できること

| ステップ | Katsuoがすること | あなたが決めること |
|---|---|---|
| 規模確認 | 変更が小さいか大きいかを判断し、最小の役に立つ機能を提案 | 取り組む範囲に合意 |
| 初期設定（初回のみ） | プロジェクトを理解し、いくつか質問して、適切なガードレールを設定 | 方針を確認 |
| 仕様 | 受け入れ条件とタスクの関係を作成 | 計画を承認 |
| 実装 | タスクごとにRed → Green → Refactor。試行は最大3回 | タスク単位または機能単位で承認 |
| レビュー | 新しい読み取り専用レビュアーが仕様、テスト、セキュリティ、シンプルさを確認 | 残った問題への対応を判断 |
| PR | 機能ブランチをpushし、Pull Requestを作成 | マージを判断 |

GitHubリポジトリでは、エージェントによる`main`/`master`へのpush、force-push、マージをフックが禁止します。これらの最終判断は、常にあなたが行います。

## インストール

**Claude Code**

```bash
claude plugin marketplace add AllBlue-inc/katsuo && claude plugin install katsuo@katsuo
```

**Codex**

```bash
codex plugin marketplace add AllBlue-inc/katsuo && codex plugin add katsuo@katsuo
```

次にCodexで`/hooks`を開き、Katsuoのフックを信頼してください。

Claude Codeでは`/katsuo`、Codexでは`$katsuo`で実行します。

フックの実行には、`PATH`上の`python3`が必要です。Pull Requestの作成には`gh` CLIを推奨します。

**更新:** `claude plugin marketplace update katsuo` · **削除:** `claude plugin uninstall katsuo@katsuo` / `codex plugin remove katsuo`

## 動作証明

```bash
python3 tests/e2e_smoke.py
python3 tests/e2e_smoke.py --live
```

最初のコマンドは、パッケージの整合性とマニフェストから実際のフックまでの経路を証明します。Claude Codeがあればパッケージを検証し、CodexがあればKatsuoが有効かも確認します。`--live`は、認証済みの両方のホストからKatsuoを実行して応答を確認します。Claudeのツールは無効にし、Codexは読み取り専用サンドボックスで実行します。認証情報は各CLI内に留まり、テストには保存されません。

**2026-10-06 検証済み:** 決定的テスト、Claude Codeのライブスモーク、Codexのライブスモークはすべて合格しました。

| 根拠 | 証明すること |
|---|---|
| CIテスト | パッケージの整合性、参照ファイル、ガードの動作、フックの接続 |
| Claude検証 | Claude Codeがプラグインを受け付けること |
| Codex検出 | CodexでKatsuoがインストール済み・有効であること |
| ライブスモーク | 合格: 両方のホストがKatsuoを読み込み実行できること |

テスト合格が証明するのは、確認した経路です。将来のすべてのモデル判断が常に同じになることまでは保証しません。

## ファイル構成

```text
skills/katsuo/SKILL.md  コマンドと作業プロセス
agents/reviewer.md      独立レビュアー（読み取り専用）
hooks/guard_git.py      PR運用を守るGitガード
tests/e2e_smoke.py      決定的テストとライブ動作証明
```

作者: Aakash
