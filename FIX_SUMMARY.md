# حل مشكلة ModuleNotFoundError: No module named 'src'

## 📋 ملخص المشكلة

كنت تواجه الخطأ التالي:
```
ModuleNotFoundError: No module named 'src'
```

السبب: المشروع يستخدم imports مثل `from src.config import get_settings` ولكن لم يكن مثبتاً كـ Python package.

---

## ✅ الحل النهائي

تم إجراء التعديلات التالية لحل المشكلة نهائياً:

### 1️⃣ الملفات المُنشأة

| الملف | الوصف |
|------|-------|
| `setup.py` | ملف إعداد المشروع (طريقة setuptools الكلاسيكية) |
| `pyproject.toml` | ملف إعداد المشروع الحديث (PEP 518) |
| `src/__init__.py` | جعل مجلد `src` package قابل للاستيراد |
| `.env.example` | مثال للمتغيرات البيئية |
| `test_installation.py` | سكريبت للتحقق من التثبيت |
| `INSTALLATION.md` | دليل التثبيت بالتفصيل |

### 2️⃣ التعديلات على الملفات الموجودة

| الملف | التعديل |
|------|---------|
| `Dockerfile` | تحديث لاستخدام pip بدلاً من uv وإضافة `pip install -e .` |
| `Makefile` | إضافة أوامر `install`, `dev-install`, `run-local` |
| `requirements.txt` | إضافة `sqlalchemy` |

---

## 🚀 خطوات التشغيل

### الخطوة 1: التثبيت (مرة واحدة فقط)

```bash
# تفعيل البيئة
conda activate voltstack

# تثبيت المشروع في وضع editable
pip install -e .
```

أو استخدم:
```bash
make install
```

### الخطوة 2: التحقق من التثبيت

```bash
python test_installation.py
```

يجب أن ترى:
```
✅ All imports working correctly!
🎉 Installation is working correctly!
```

### الخطوة 3: التشغيل

#### أ) التشغيل المحلي (بدون Docker)

```bash
# الطريقة الأولى
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# الطريقة الثانية
make run-local

# الطريقة الثالثة
python -m src.main
```

#### ب) التشغيل باستخدام Docker

```bash
# بناء وتشغيل جميع الخدمات
make up

# عرض السجلات
make logs

# إيقاف الخدمات
make down
```

---

## 🔍 كيف يعمل الحل؟

### قبل الحل ❌
```
المشروع
├── src/
│   ├── main.py  → from src.config import ...  ❌ لا يعمل
│   └── config.py
```
Python لا يعرف أين يجد module اسمه `src`.

### بعد الحل ✅
```
المشروع
├── setup.py              ← يخبر Python أن هذا package
├── pyproject.toml        ← معايير حديثة
├── src/
│   ├── __init__.py       ← يجعل src قابل للاستيراد
│   ├── main.py  → from src.config import ...  ✅ يعمل!
│   └── config.py
```

عند تشغيل `pip install -e .`:
- ✅ يضيف مسار المشروع إلى PYTHONPATH
- ✅ يصبح `src` قابل للاستيراد من أي مكان
- ✅ التغييرات في الكود تظهر فوراً (editable mode)

---

## 📦 الـ Dependencies المثبتة

```
fastapi           - Web framework
uvicorn          - ASGI server
psycopg2-binary  - PostgreSQL driver
opensearch-py    - OpenSearch client
pydantic         - Data validation
pydantic-settings - Settings management
python-dotenv    - .env file support
sqlalchemy       - ORM
```

---

## 🛠️ الأوامر المفيدة

```bash
# عرض جميع الأوامر
make help

# تثبيت المشروع
make install

# تثبيت مع أدوات التطوير
make dev-install

# تشغيل محلي
make run-local

# بناء Docker
make build

# تشغيل Docker
make up

# عرض السجلات
make logs

# إيقاف الخدمات
make down

# اختبار التثبيت
python test_installation.py
```

---

## 🧪 اختبار سريع

```bash
# اختبار الـ imports
python -c "from src.config import get_settings; print('✓ Working!')"

# عرض الإعدادات
python -c "from src.config import get_settings; print(get_settings())"

# تشغيل السكريبت الكامل
python test_installation.py
```

---

## ⚠️ ملاحظات مهمة

1. **يجب تشغيل `pip install -e .` مرة واحدة فقط** بعد:
   - استنساخ المشروع لأول مرة
   - تغيير بيئة Python
   - حذف البيئة وإعادة إنشائها

2. **إضافة dependencies جديدة**: إذا أضفت مكتبات جديدة:
   ```bash
   # أضف للملفات:
   # - requirements.txt
   # - setup.py (في install_requires)
   # - pyproject.toml (في dependencies)
   
   # ثم أعد التثبيت:
   pip install -e .
   ```

3. **Docker**: يتم التثبيت تلقائياً عند بناء الـ image، لا حاجة لأي خطوات إضافية.

4. **Git**: لا تنسى إضافة `.env` إلى `.gitignore` (استخدم `.env.example` للمشاركة).

---

## 🎯 الخلاصة

المشكلة تم حلها بالكامل من خلال:
- ✅ إنشاء `setup.py` و `pyproject.toml`
- ✅ إضافة `src/__init__.py`
- ✅ تشغيل `pip install -e .`
- ✅ تحديث `Dockerfile` و `Makefile`
- ✅ إضافة سكريبت اختبار

الآن يمكنك:
- ✅ استيراد أي module من `src` من أي مكان
- ✅ تشغيل المشروع محلياً أو عبر Docker
- ✅ التطوير براحة بدون مشاكل imports

---

## 📚 موارد إضافية

- [Python Packaging User Guide](https://packaging.python.org/)
- [setuptools Documentation](https://setuptools.pypa.io/)
- [PEP 518 – pyproject.toml](https://peps.python.org/pep-0518/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

**آخر تحديث:** يناير 2026
**الحالة:** ✅ تم الحل نهائياً
