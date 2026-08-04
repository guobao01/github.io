# 甲基化检测试剂盒获批情况统计

NMPA 甲基化检测试剂盒注册审批数据汇总展示页面，支持 Excel 数据更新后自动同步网页。

## 项目结构

```
methylation-kit-tracker/
├── index.html                              # 网页页面
├── generate_data.py                        # Excel → JS 数据转换脚本
├── watch.py                                # 本地文件监控脚本（自动同步）
├── requirements.txt                        # Python 依赖
├── 甲基化检测试剂盒获批情况统计.xlsx          # 源数据文件
├── data.js                                 # 自动生成的数据文件（勿手动修改）
├── data.json                               # 备用数据文件（自动生成）
└── .github/workflows/deploy.yml            # GitHub Actions 自动部署工作流
```

## 数据同步说明

网页读取的是 `data.js`（由 `generate_data.py` 从 Excel 生成），**不是直接读取 Excel**。
因此修改 Excel 后，需要重新生成 `data.js` 才能同步到网页。

### 方式一：本地自动监控（推荐）

运行监控脚本，修改 Excel 后自动同步：

```bash
python watch.py
```

- 监控项目目录和桌面的 Excel 文件
- 检测到修改后自动运行 `generate_data.py` 重新生成 `data.js`
- 生成后点击网页上的"刷新数据"按钮即可看到更新
- 按 `Ctrl+C` 停止监控

### 方式二：手动重新生成

```bash
python generate_data.py
```

然后刷新网页或点击"刷新数据"按钮。

### 方式三：GitHub 自动同步

修改 Excel 后推送到 GitHub，Actions 自动重新生成并部署。

## 快速开始

### 1. 创建 GitHub 仓库

在 GitHub 上创建一个新仓库（例如 `methylation-kit-tracker`）。

### 2. 上传项目文件

将本目录下所有文件上传到仓库：

```bash
cd methylation-kit-tracker
git init
git add .
git commit -m "初始化：甲基化检测试剂盒获批统计网页"
git branch -M main
git remote add origin https://github.com/你的用户名/methylation-kit-tracker.git
git push -u origin main
```

### 3. 启用 GitHub Pages

1. 进入仓库的 **Settings → Pages**
2. **Source** 选择 **GitHub Actions**
3. 保存后，首次推送会自动触发部署

### 4. 访问网页

部署完成后，访问：
```
https://你的用户名.github.io/methylation-kit-tracker/
```

## 日常更新流程

当你修改了 Excel 文件后：

```bash
# 1. 将更新后的 Excel 复制到项目目录
cp ~/Desktop/甲基化检测试剂盒获批情况统计.xlsx .

# 2. 提交并推送
git add 甲基化检测试剂盒获批情况统计.xlsx
git commit -m "更新数据：新增/修改试剂盒记录"
git push
```

推送后 GitHub Actions 会自动重新生成网页，约 1-2 分钟后刷新页面即可看到更新。

## 网页功能

- 实时搜索（试剂盒名称、公司、靶标、注册证编号）
- 按癌种、样本类型、审评报告筛选
- 点击表头排序
- 统计概览卡片
- 性能指标可视化（灵敏度、特异性、准确度）
- 响应式设计，支持手机浏览
