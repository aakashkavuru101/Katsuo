# katsuo

[![Tests](https://github.com/AllBlue-inc/Katsuo/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/AllBlue-inc/Katsuo/actions/workflows/test.yml)

[English](README.md) | **日本語**

Claude Code と Codex 用の開発プラグインです。答えを先に伝え、手順は短く、話を脇道にそらしません。仕様 → テスト駆動開発 → 独立レビュー → Pull Request の順に作業を進めます。

## インストール

**Claude Code**

```bash
claude plugin marketplace add AllBlue-inc/katsuo && claude plugin install katsuo@katsuo
```

**Codex**

```bash
codex plugin marketplace add AllBlue-inc/katsuo && codex plugin add katsuo@katsuo
```

Codexでは、インストール後に`/hooks`を開いてKatsuoのフックを信頼してください。

フックの実行には`PATH`上の`python3`が必要です。Pull Requestの作成には`gh` CLIを推奨します。

**更新:** `claude plugin marketplace update katsuo` · **削除:** `claude plugin uninstall katsuo@katsuo` / `codex plugin remove katsuo`

## 使い方

Claude Codeでは`/katsuo`、Codexでは`$katsuo`の後ろに、作りたいものを書きます。

```text
/katsuo メールによるパスワードリセットを追加
```

1. Katsuoが変更を Small か Big に分け、最初に作る機能を提案します。範囲に合意してください。
2. 初回だけ、プロジェクトについて質問されます（一度に最大3問）。答えると `docs/project.md` と `AGENTS.md` が作られます。
3. 受け入れ条件とタスク一覧（`docs/specs/<名前>.md`）を承認します。
4. Katsuoがタスクごとにテストを書いてから実装します。1タスクの試行は最大3回で、超えたら相談されます。
5. 読み取り専用のレビュアーが差分を確認し、問題があれば修正されます。
6. Pull Requestのリンクが届きます。マージはあなたが行います。

エージェントによる`main`/`master`へのpush、force-push、マージはフックで禁止しています。

## 開発者向け

### テスト

```bash
python3 tests/e2e_smoke.py          # パッケージとフックの接続を確認
python3 tests/e2e_smoke.py --live   # 認証済みの Claude Code と Codex で実際に実行
```

### ファイル構成

```text
skills/katsuo/SKILL.md  コマンドと作業手順
agents/reviewer.md      独立レビュアー（読み取り専用）
hooks/guard_git.py      Git操作のガード
tests/e2e_smoke.py      決定的テストとライブテスト
```

作者: Aakash
