# application-library-management
A project for managing library books, members, and borrowing system.
add,delete,modify books by the employee
borrow,reservation and purchase by subscribed client
looking for a book by the user
and register new client and login/log out for subscribed client and employee 
بالعربي:
Library Management System (API)
نظام متكامل لإدارة الكتب، الأعضاء، وعمليات الاستعارة والبيع، مبني باستخدام Django REST Framework.

 المميزات الأساسية (Core Features)
 قسم الموظفين (Employee Panel)
إدارة الكتب: إضافة، حذف، وتعديل بيانات الكتب.

تتبع العمليات (Action Log): تسجيل تلقائي لأي عملية إضافة أو تعديل تتم على الكتب لضمان الشفافية.

إدارة المخزون: تحديث تلقائي لحالة الكتاب (Available/Not Available) بناءً على الكمية المتوفرة.

 قسم المشتركين (Subscribed Clients)
البحث المتقدم: إمكانية البحث عن الكتب حسب العنوان أو المؤلف عبر الـ API.

نظام الاستعارة (Borrowing): استعارة الكتب مع حساب تلقائي لتاريخ الإرجاع (5 أيام).

الحجز (Reservation): إمكانية حجز الكتب غير المتوفرة حالياً بنظام الأولوية حسب التاريخ.

الشراء والتقييم: شراء الكتب وتقييمها من 1 إلى 5 نجوم مع إضافة تعليقات.

نظام الدفع: توثيق عمليات الدفع لمختلف الخدمات (Credit Card, PayPal, Cash).

🛠 التقنيات المستخدمة (Tech Stack)
Backend: Django & Django REST Framework.

Database: SQLite (Development).

Authentication: Django Built-in Auth System (Login/Logout/Registration).

 كيفية التشغيل (Setup)
قم بتفعيل البيئة الافتراضية: venv\Scripts\activate.

قم بتثبيت المكتبات المطلوبة: pip install -r requirements.txt.

قم بتحديث قاعدة البيانات: python manage.py migrate.

قم بتشغيل السيرفر: python manage.py runserver.