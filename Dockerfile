# استفاده از آخرین نسخه LTS پایتون
FROM python:3.12-bookworm

# تنظیم محیط
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# نصب وابستگی‌ها
COPY ./backend/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# کپی پروژه
COPY ./backend /app/