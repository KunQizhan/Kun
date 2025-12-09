# Kun

[English](#english) | [简体中文](#简体中文)

---

## 简体中文

### 项目简介

**Kun** 是我的个人技术与学习仓库，主要以 **Jupyter Notebook（约 98.6%）** 为主。  
这里会陆续整理和更新：

- 个人独立开发的项目（Personal Projects）
- 参加各类比赛/竞赛的代码与笔记（Competitions）
- 课程相关的课件、作业与实验（Courses & Assignments）
- 自学过程中的实验与探索（Self-learning Experiments）

> 当前部分内容尚未上传或仍在整理中，仓库会持续更新迭代。

---

### 内容规划

仓库计划按功能与来源进行分类管理，示例结构如下，具体以实际为准：

```text
Kun/
├─ projects/              # 个人项目（未来持续更新）
│  ├─ project_name_1/
│  └─ project_name_2/
├─ competitions/          # 参加的比赛/竞赛
│  ├─ kaggle_xxx/
│  ├─ ai_competition_xxx/
│  └─ ...
├─ courses/               # 课程课件与作业
│  ├─ course_name_1/
│  │  ├─ lectures/        # 课件 & 笔记
│  │  └─ assignments/     # 作业 & 实验
│  └─ course_name_2/
├─ experiments/           # 自学实验（算法/模型/小想法）
│  ├─ ml_basics.ipynb
│  ├─ dl_try_xxx.ipynb
│  └─ ...
├─ data/                  # 示例数据（如有，部分可能被 .gitignore 忽略）
├─ images/                # 图片或可视化结果
└─ README.md
```

> 随着内容增加，目录结构可能会调整，以保持清晰和可维护性。

---

### 技术方向（可能涉及）

根据 Notebook 内容，仓库可能会涉及但不限于：

- 数据分析与可视化（Pandas / Matplotlib / Seaborn 等）
- 机器学习与深度学习基础
- 各类比赛的特定任务（如分类、回归、NLP、CV 等）
- 课程相关的理论与实验实现
- 自主探索的一些小 Demo / 实验性项目

具体技术栈会在各子目录或 Notebook 中进一步说明。

---

### 环境与依赖

#### 1. 基础环境

建议：

- Python：`3.9+`（或与实际项目一致的版本）
- 推荐工具：
  - [Anaconda](https://www.anaconda.com/) / [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
  - [JupyterLab](https://jupyter.org/) 或经典版 [Jupyter Notebook](https://jupyter.org/)

#### 2. 创建虚拟环境（示例）

```bash
# 使用 conda
conda create -n kun python=3.9
conda activate kun

# 或使用 venv
python -m venv .venv
source .venv/bin/activate  # Windows 使用 .venv\Scripts\activate
```

#### 3. 安装依赖

如果仓库中提供了 `requirements.txt` 或 `environment.yml`：

```bash
# pip
pip install -r requirements.txt

# conda
conda env create -f environment.yml
conda activate kun
```

如果暂时没有统一依赖文件，可根据各个 Notebook 中的 `import` 语句按需安装，例如：

```bash
pip install numpy pandas matplotlib seaborn scikit-learn
```

---

### 使用方式

1. **克隆仓库**

   ```bash
   git clone https://github.com/KunQizhan/Kun.git
   cd Kun
   ```

2. **选择感兴趣的模块**

   - `projects/`：查看个人项目的整体设计与实现
   - `competitions/`：查看比赛的解题思路、特征工程和模型方案
   - `courses/`：查看课程作业与相关实验
   - `experiments/`：查看自学过程中的各种尝试和小实验

3. **启动 Jupyter**

   ```bash
   jupyter lab
   # 或
   jupyter notebook
   ```

4. **运行 Notebook**

   - 打开对应目录下的 `.ipynb` 文件
   - 建议按文件内给出的顺序或说明依次运行单元格
   - 如遇缺包或数据路径错误，根据报错信息进行安装或修改

---

### 适合谁看？

- 想了解我在做什么项目、参加过什么比赛
- 对课程作业实现、学习路径感兴趣的同学
- 希望参考个人学习与实践笔记的同学
- 未来可能一起合作项目或组队比赛的伙伴

---

### 未来计划

- 持续整理并上传已有的个人项目与比赛代码
- 为课程和作业补充更完善的说明文档和注释
- 增加更多自学实验（如新模型尝试、论文复现、小工具等）
- 逐步优化目录结构和代码质量

---

### 许可证

许可证类型会在内容稳定后统一补充。  
在此之前，默认用于 **学习与交流**，如需在其它场景中使用或引用，欢迎提前与我联系。

---

## English

### Overview

**Kun** is my personal repository for **projects, competitions, courses, and self-learning experiments**, mainly based on **Jupyter Notebooks (~98.6%)**.

This repo will gradually include:

- Personal projects (independent development)
- Code and notes from competitions
- Course materials, assignments, and experiments
- Experiments and explorations from self-study

> Some parts are not uploaded yet or still being organized. The repository will be updated continuously.

---

### Planned Contents

The repository is organized by purpose and source. A planned structure looks like this (subject to change):

```text
Kun/
├─ projects/              # Personal projects (more to come)
│  ├─ project_name_1/
│  └─ project_name_2/
├─ competitions/          # Competitions I participated in
│  ├─ kaggle_xxx/
│  ├─ ai_competition_xxx/
│  └─ ...
├─ courses/               # Course materials & assignments
│  ├─ course_name_1/
│  │  ├─ lectures/        # Slides & notes
│  │  └─ assignments/     # Homework & experiments
│  └─ course_name_2/
├─ experiments/           # Self-learning experiments
│  ├─ ml_basics.ipynb
│  ├─ dl_try_xxx.ipynb
│  └─ ...
├─ data/                  # Sample data (some may be git-ignored)
├─ images/                # Figures & visualization outputs
└─ README.md
```

As the content grows, the structure may be adjusted to keep it clean and maintainable.

---

### Possible Technical Topics

Depending on the notebooks, this repo may cover (but is not limited to):

- Data analysis & visualization (Pandas / Matplotlib / Seaborn, etc.)
- Machine learning & deep learning basics
- Competition-specific tasks (classification, regression, NLP, CV, etc.)
- Course-related theory and experiments
- Small demos and experimental ideas from self-learning

More details will be given inside each folder or notebook.

---

### Environment & Dependencies

#### 1. Basic environment

Recommended:

- Python: `3.9+` (or the actual version used by the projects)
- Tools:
  - [Anaconda](https://www.anaconda.com/) / [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
  - [JupyterLab](https://jupyter.org/) or classic [Jupyter Notebook](https://jupyter.org/)

#### 2. Create a virtual environment (example)

```bash
# Using conda
conda create -n kun python=3.9
conda activate kun

# Or using venv
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

#### 3. Install dependencies

If `requirements.txt` or `environment.yml` is provided:

```bash
# pip
pip install -r requirements.txt

# conda
conda env create -f environment.yml
conda activate kun
```

If there is no unified dependency file yet, install packages according to imports in each notebook, for example:

```bash
pip install numpy pandas matplotlib seaborn scikit-learn
```

---

### How to Use

1. **Clone the repo**

   ```bash
   git clone https://github.com/KunQizhan/Kun.git
   cd Kun
   ```

2. **Pick what you are interested in**

   - `projects/`: personal project design and implementations
   - `competitions/`: competition solutions, feature engineering, and models
   - `courses/`: course assignments and experiments
   - `experiments/`: various trials and small experiments from self-learning

3. **Launch Jupyter**

   ```bash
   jupyter lab
   # or
   jupyter notebook
   ```

4. **Run the notebooks**

   - Open the `.ipynb` files in the corresponding folder
   - Follow the suggested order or instructions inside the notebook
   - If you hit missing packages or path issues, install or adjust accordingly

---

### Who Might Find This Useful

- Anyone who wants to see what projects and competitions I’ve worked on
- Students interested in course assignments and implementation details
- People looking for reference learning paths or personal study notes
- Potential collaborators or teammates for future projects/competitions

---

### Future Plans

- Keep uploading and整理 existing personal projects & competition code
- Add better documentation and comments for courses and assignments
- Add more self-learning experiments (new models, paper reproduction, small tools, etc.)
- Gradually improve the folder structure and code quality

---

### License

The final license will be added once the content becomes more stable.  
Before that, the repo is mainly for **learning and sharing**.  
If you’d like to use or reference it in other scenarios, feel free to contact me first.
