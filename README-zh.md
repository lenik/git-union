# git-union

**git-union** 是一个用于将多个 Git 仓库合并为 **单一 Monorepo** 的工具。
每个原始仓库会被放入 Monorepo 的一个子目录中，并保留完整的提交历史。

适用于：

* 多仓库项目迁移到 **Monorepo**
* 合并多个历史项目
* 整理分散的代码仓库

---

# 安装

当前仓库提供可直接执行的 `git-union` 脚本。

从仓库安装：

```bash
chmod +x ./git-union
sudo install -m 0755 ./git-union /usr/local/bin/git-union
```

使用 Debian 打包安装：

```bash
dpkg-buildpackage -us -uc
sudo dpkg -i ../git-union_*.deb
```

---

# 使用方法

```bash
git-union [OPTIONS] MONO_DIR REPO...
```

## 参数

### `MONO_DIR`

要创建的 **Monorepo 目录**。

执行后将在该目录中创建新的 Git 仓库：

```
MONO_DIR/.git
```

---

### `REPO`

需要合并的仓库。

支持两种写法：

#### 1️⃣ 直接指定仓库路径

```bash
git-union mono foo bar
```

子目录名称将使用仓库路径的 **basename**：

```
mono/
    foo/
    bar/
```

---

#### 2️⃣ 指定子目录名称

```bash
git-union mono core=foo ui=bar
```

结果：

```
mono/
    core/
    ui/
```

---

# 示例

假设有两个仓库：

```
foo/.git
bar/.git
```

执行：

```bash
git-union monodir foo bar
```

生成新的仓库：

```
monodir/
    .git
    foo/
    bar/
```

---

# 选项

### `-s, --sort`

按照 **author time** 对不同仓库的提交进行交叉排序。

规则：

* **保持同一个仓库内部的提交顺序不变**
* 不同仓库之间的提交可以交叉排列

例如：

```
repo1: 10 21 45 33 51
repo2:  8 13 31 49
```

合并后的可能结果：

```
mono: 8 10 13 21 31 45 33 49 51   (推荐)
mono: 8 10 13 21 31 45 49 33 51   (也合法)
```

注意：

```
45 -> 33
```

这个顺序不会被改变，因为它们来自同一个仓库。

由于约束条件的存在，可能存在多个合法解。
程序会尽量选择 **看起来最接近时间排序的结果**。

---

### `-v, --verbose`

输出详细日志。

---

### `-q, --quiet`

减少输出，仅显示错误。

---

### `-h, --help`

显示帮助信息。

---

### `--version`

显示版本信息。

---

# 设计目标

git-union 的目标是：

* **简单**：只解决 Monorepo 合并问题
* **保持历史**：所有原始提交完整保留
* **可读历史**：支持按时间排序让历史更自然

---

# 测试

运行自动化测试：

```bash
python3 -m unittest -v
```

测试会在临时目录中创建多个 Git 仓库并验证：

* 基础合并流程是否正确
* `name=repo` 映射是否生效
* `--sort` 是否在跨仓库排序时仍保持单仓库内部顺序

快速手工验证（可选）：

```bash
./git-union --help
./git-union --version
```

---

# 许可证（2026）

版权所有 (C) 2026 Lenik（`git-union@bodz.net`）

本项目使用 **GNU Affero General Public License**，版本 3 或更高版本（**AGPL-3.0-or-later**）。
详见 `LICENSE`。

## Anti-AI 声明（项目政策，非法律约束）

作为额外的**非约束性**项目政策声明：作者请求不要在未获得明确许可的情况下，使用本项目来训练或评估机器学习模型。
该声明不旨在对 AGPL 许可证条款之外增加额外的法律限制。

