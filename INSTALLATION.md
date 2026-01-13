# RAG Service - حل مشكلة الـ Imports

## المشكلة
كنت تواجه خطأ `ModuleNotFoundError: No module named 'src'` لأن المشروع لم يكن مثبتاً كـ package.

## الحل
تم إنشاء الملفات التالية لحل المشكلة نهائياً:

1. **`setup.py`** - ملف إعداد المشروع الكلاسيكي
2. **`pyproject.toml`** - ملف إعداد المشروع الحديث (PEP 518)
3. **`src/__init__.py`** - ملف لجعل `src` package

## طرق التشغيل

### 1. التثبيت كـ Package (مطلوب - مرة واحدة فقط)

```bash
# تفعيل البيئة
conda activate voltstack

# تثبيت المشروع في وضع التطوير (editable mode)
pip install -e .

# أو استخدام Makefile
make install
```

### 2. التشغيل المحلي (بدون Docker)

```bash
# الطريقة الأولى - مباشرة
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# الطريقة الثانية - باستخدام Makefile
make run-local
```

### 3. التشغيل باستخدام Docker

```bash
# بناء وتشغيل جميع الخدمات
make up

# عرض السجلات
make logs

# إيقاف الخدمات
make down
```

## كيف يعمل الحل؟

عند تشغيل `pip install -e .`:
- يتم إضافة مسار المشروع إلى Python path
- يصبح بإمكانك استيراد `src` من أي مكان في المشروع
- أي تغييرات في الكود تظهر فوراً بدون إعادة التثبيت (editable mode)

## الأوامر المفيدة

```bash
# عرض جميع الأوامر المتاحة
make help

# تثبيت المشروع مع أدوات التطوير
make dev-install

# تشغيل الـ API محلياً
make run-local
```

## اختبار أن كل شيء يعمل

```bash
python -c "from src.config import get_settings; print(get_settings())"
```

إذا لم يظهر خطأ، فإن المشكلة تم حلها! ✅

## ملاحظات مهمة

- يجب تشغيل `pip install -e .` **مرة واحدة فقط** بعد استنساخ المشروع
- إذا أضفت dependencies جديدة في `requirements.txt` أو `setup.py`، قم بإعادة التثبيت
- في Docker، يتم التثبيت تلقائياً عند بناء الـ image
