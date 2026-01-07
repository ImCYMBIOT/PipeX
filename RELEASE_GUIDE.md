# PipeX Release Guide

## 🎯 **Current Setup: Manual Release Only**

We're starting simple with just manual releases to PyPI. Once this works, we'll add CI/CD and automation.

## 📋 **Prerequisites**

### **1. PyPI Trusted Publishing Setup (Required)**

You need to set up trusted publishing on PyPI:

1. **Go to PyPI**: https://pypi.org/manage/account/publishing/
2. **Add a new publisher**:
   - **PyPI Project Name**: `pipex` (or whatever you want to call it)
   - **Owner**: `ImCYMBIOT` (your GitHub username)
   - **Repository name**: `PipeX` (your repo name)
   - **Workflow filename**: `python-publish.yml`
   - **Environment name**: `pypi`

### **2. GitHub Environment Setup (Recommended)**

1. **Go to GitHub**: Your repo → Settings → Environments
2. **Create environment**: `pypi`
3. **Add protection rules** (optional but recommended):
   - Require reviewers
   - Wait timer
   - Deployment branches (only main/master)

## 🚀 **How to Release**

### **Step 1: Prepare for Release**

```bash
# 1. Make sure your code is ready
git status
git add .
git commit -m "feat: prepare for v2.0.0 release"
git push origin main

# 2. Test locally (optional but recommended)
poetry install --all-extras
poetry run pipex --help
poetry build
ls -la dist/
```

### **Step 2: Create GitHub Release**

1. **Go to GitHub**: Your repo → Releases → "Create a new release"
2. **Choose a tag**: `v2.0.0` (create new tag)
3. **Release title**: `PipeX v2.0.0 - Multi-Cloud ETL Pipeline`
4. **Description**: Use content from CHANGELOG.md or write:

   ````markdown
   ## What's New in v2.0.0

   🚀 **Major Features:**

   - Multi-cloud storage support (AWS S3, Google Cloud, Azure, DigitalOcean)
   - Enhanced file format support (Excel, Parquet, XML)
   - Intelligent error handling with actionable solutions
   - Advanced transformation system with industry templates
   - Performance optimization for large datasets

   ## Installation

   ```bash
   pip install pipex==2.0.0
   ```
   ````

   ## Documentation

   See [README.md](https://github.com/ImCYMBIOT/PipeX/blob/main/README.md) for full documentation.

   ```

   ```

5. **Click "Publish release"**

### **Step 3: Monitor the Workflow**

1. **Go to Actions tab** in your GitHub repo
2. **Watch the "Upload Python Package" workflow**
3. **Check each step**:
   - ✅ Validate pyproject.toml
   - ✅ Install dependencies
   - ✅ Test basic imports
   - ✅ Build distributions
   - ✅ Publish to PyPI

### **Step 4: Verify Publication**

1. **Check PyPI**: https://pypi.org/project/pipex/
2. **Test installation**:
   ```bash
   pip install pipex==2.0.0
   pipex --help
   ```

## 🔧 **Troubleshooting**

### **Common Issues:**

#### **1. Trusted Publishing Not Set Up**

```
Error: Trusted publishing exchange failure
```

**Solution**: Set up trusted publishing on PyPI (see prerequisites)

#### **2. Environment Not Found**

```
Error: Environment 'pypi' not found
```

**Solution**: Create the `pypi` environment in GitHub repo settings

#### **3. Import Errors**

```
Error: ModuleNotFoundError: No module named 'app'
```

**Solution**: Check that all files are committed and pushed to GitHub

#### **4. Build Errors**

```
Error: poetry build failed
```

**Solution**: Test locally first with `poetry build`

### **Debug Steps:**

1. **Check workflow logs** in GitHub Actions
2. **Test locally** with the same commands
3. **Verify pyproject.toml** is valid
4. **Check all files are committed**

## 📈 **Next Steps (After First Release Works)**

Once the manual release works, we can add:

1. **✅ Manual Release** (Current - what we're testing)
2. **🔄 CI Workflow** - Test on every PR
3. **🚀 Auto Release** - Release on version tags
4. **📦 Dependabot** - Automatic dependency updates
5. **🔍 Code Quality** - Linting, type checking, security scans

## 🎉 **Success Checklist**

After a successful release, you should see:

- ✅ GitHub release created with assets
- ✅ Package published on PyPI
- ✅ `pip install pipex==2.0.0` works
- ✅ `pipex --help` shows your CLI

## 💡 **Tips**

- **Start with a test version** like `v2.0.0-beta.1` first
- **Use semantic versioning**: `v2.0.0`, `v2.0.1`, `v2.1.0`
- **Keep release notes clear** and user-focused
- **Test the package** after publishing

Ready to release PipeX v2.0.0? 🚀
