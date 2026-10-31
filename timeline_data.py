# -*- coding: utf-8 -*-
"""Timeline v5: each step's description lives INSIDE the branch lane it belongs to
(no bottom strip). Labels are anchored at the far (left/time) end of the bar and grow
upward, so a finished deck reads as one cumulative timeline per branch.
Three full-page product cards (SER / MRT / دیتادیود) sit right after the combination step.
Technical terms are written in Latin script, as requested."""

LANES = [
    dict(key="الکترونیک", sub="سخت‌افزار، Firmware، Embedded Linux", color="#3D6DA8"),
    dict(key="اتوماسیون صنعتی", sub="DCS، PLC، صنعت برق، پست و نیروگاه", color="#4F7E63"),
    dict(key="هوش مصنوعی", sub="از شبکه‌های عصبی تا LLM و Agent", color="#7B5FA6"),
    dict(key="نرم‌افزار", sub="از وب تا معماری سیستم", color="#2F8CAD"),
]
UMB_COLOR = "#2C3138"

# page identity: shown on the cover page and on the closing page
OWNER = dict(
    name="حامد دونده",
    kick="مهندس سیستم",
    lead="مسیر حرفه‌ای: چهار شاخه زیر یک چتر",
    last_edit="۹ آبان ۱۴۰۵",
    linkedin="https://www.linkedin.com/in/hamed-davandeh/",
)

# h = cumulative thickness (0..9, monotonic, never decreases)
# grow = lane(s) thickened at this step   |   ev = [(lane, label)] shown ONLY for this step
# pg = full-page product card (title, tag, points, role)
STEPS = [
    dict(hero=True, cap="", h=[0, 0, 0, 0], grow=[], ev=[]),
    dict(cap="چهار سطر، چهار شاخه؛ در هر گام یک شاخه قطورتر می‌شود",
         h=[0, 0, 0, 0], grow=[], ev=[], yr="۱۳۸۲"),
    dict(cap="دانشگاه فردوسی مشهد", h=[2.5, 0, 0, 0], grow=[0],
         ev=[(0, "لیسانس الکترونیک؛ تدریس و آزمایشگاه؛ R&D دانشگاه سجاد")], yr="۱۳۸۳"),
    dict(cap="شبکه‌های عصبی، از لیسانس تا ارشد", h=[2.5, 0, 3.5, 0], grow=[2],
         ev=[(2, "درس شبکه‌های عصبی (۸۲-۸۳)؛ مقاله‌های GA؛ پایان‌نامه‌ی شبکه‌های عصبی جاذب")], yr="۱۳۸۵-۱۳۸۷"),
    dict(cap="فاصله‌ی بین لیسانس و ارشد", h=[2.5, 0, 3.5, 2], grow=[3],
         ev=[(3, "PHP و MySQL؛ اولین درآمد حرفه‌ای از طراحی وب (۵۰ هزار تومان)")], yr="۱۳۸۳-۱۳۸۵"),
    dict(cap="طلیعه شرق | گروه مهام شرق", h=[5, 0, 3.5, 2], grow=[0],
         ev=[(0, "سخت‌افزار و Firmware؛ مهندسی معکوس آلارم‌یونیت؛ طراحی PCB")], yr="۱۳۸۸"),
    dict(cap="طلیعه شرق: حضور در پست‌های انتقال", h=[5, 2, 3.5, 2], grow=[1],
         ev=[(1, "چند پست انتقال؛ پست ۴۰۰ کیلوولت سهند تبریز برای رفع عیب آلارم‌یونیت‌ها")], yr="۱۳۸۹"),
    dict(cap="طلیعه شرق: ورود به اتوماسیون", h=[5, 3.5, 3.5, 2], grow=[1],
         ev=[(1, "Remote-IO روی Modbus/TCP؛ وصل به iFIX؛ IEC 61850 و PROFIBUS")], yr="۱۳۹۰"),
    dict(cap="MAPCS", h=[7, 3.5, 3.5, 2], grow=[0],
         ev=[(0, "Raspberry Pi؛ Embedded Linux؛ Modbus/TCP Gatewayها")], yr="۱۳۹۱"),
    dict(cap="MAPCS: عمق در اتوماسیون", h=[7, 5.5, 3.5, 2], grow=[1],
         ev=[(1, "DCS؛ Codesys و توسعه‌ی Runtime؛ دوره‌ی PROFIBUS در دوبی")], yr="۱۳۹۴-۱۳۹۶"),
    dict(cap="MAPCS: تجربه‌ی میدانی، نیروگاه حیدریه (نجف)", h=[7, 7.5, 3.5, 2], grow=[1],
         ev=[(1, "نزدیک دو ماه، طی چند مرحله، در نیروگاه حیدریه (نجف)")], yr="۱۳۹۳"),
    dict(cap="MAPCS: نرم‌افزار و روش", h=[7, 7.5, 3.5, 4.5], grow=[3],
         ev=[(3, "Scrum (اولین معرفی در مِکو)؛ Kanban؛ پیشنهاد وب و HTML5")], yr="۱۳۹۶"),
    dict(cap="محصول: ترکیب سه شاخه",
         h=[9, 9, 3.5, 6.5], grow=[0, 1, 3],
         ev=[(0, "سخت‌افزار و Firmware SER و دیتادیود صنعتی"),
             (1, "کاربرد: اتوماسیون صنعتی؛ زمان‌گذاری ۱ میلی‌ثانیه در نیروگاه‌ها"),
             (3, "نرم‌افزار و وب‌اینترفیس (Flask)؛ گروه NPD")],
         combo=True, yr="۱۳۹۷"),
    dict(cap="محصول ۱ از ۳", h=[9, 9, 3.5, 6.5], grow=[],
         ev=[(0, "SER: سخت‌افزار و Firmware"), (3, "نرم‌افزار وب و پیکربندی")],
         pg=dict(title="SER",
                 tag="ثبت‌کننده‌ی رخداد (Event Recorder) با دقت زمان‌گذاری ۱ میلی‌ثانیه",
                 points=["محصولات MAPCS در حوزه‌ی DCS بود؛ به دلیل Time Cycle حداقل ۵۰ میلی‌ثانیه، برای تحلیل Trip کافی نبود",
                         "محصولی ساختیم که با دقت ۱ میلی‌ثانیه زمان‌گذاری می‌کرد",
                       "طراحی REST API برای ارتباط با سرورهای MAPCS",
                         "تقریباً در همه‌ی نیروگاه‌های MAPCS ثابت شد و کامنت‌های زیادی از آن پروژه بسته شد"],
                 role="سخت‌افزار و Firmware + کاربرد اتوماسیون صنعتی + نرم‌افزار وب و REST API")),
    dict(cap="محصول ۲ از ۳", h=[9, 9, 3.5, 6.5], grow=[],
         ev=[(0, "MRT: Raspberry Pi و Firmware"), (1, "جایگزین ارزان‌تر پردازنده‌ی DCS")],
         pg=dict(title="MRT | MAPCS RTU Technology",
                 tag="RTU و SCADA روی Raspberry Pi Industrial Compute Modules، به‌جای پردازنده‌ی گران DCS",
                 points=[  "پردازنده‌ی DCS موجود برای کار سیستم‌های RTU و SCADA خیلی گران تمام می‌شد؛ محصول ما هزینه را محسوس پایین آورد",
                         "باعث شد شاخه‌ی جدید RTU و SCADA در MAPCS شکل بگیرد",
                         "نرم‌افزار ویندوزبیس آن با پروتکل‌های متعدد SCADA کار می‌کرد؛ من هد هر دو بخش توسعه‌ی محصول و MRT بودم"],
                 role="الکترونیک و Embedded Linux + اتوماسیون صنعتی و SCADA + نرم‌افزار ویندوزبیس")),
    dict(cap="محصول ۳ از ۳", h=[9, 9, 3.5, 6.5], grow=[],
         ev=[(0, "دیتادیود: سخت‌افزار و Firmware"), (1, "انتقال ایزوله در اتوماسیون")],
         pg=dict(title="دیتادیود صنعتی (Data Diode)",
                 tag="انتقال Modbus به Modbus، اما ایزوله",
                 points=["پیشنهاد اولیه‌اش از من بود و در قالب پروژه‌های R&D MAPCS ساخته و پشتیبانی شد",
                         "داده از مرز شبکه‌ی ایزوله عبور می‌کند، بدون آنکه ایزولاسیون شکسته شود"],
                 role="سخت‌افزار و Firmware + کاربرد اتوماسیون صنعتی + نرم‌افزار پیکربندی")),
    dict(cap="نگه‌داشت ارتباط با هوش مصنوعی", h=[9, 9, 6.5, 6.5], grow=[2],
         ev=[(2, "دوره‌ی دکتر جفری هینتون؛ بازنگری Deep-Learning و CNN")], yr="۱۳۹۸"),
    dict(cap="حلقه‌ی گمشده: چرا مهندسی سیستم؟", h=[9, 9, 6.5, 6.5], grow=[], ev=[],
         think=True, yr="۱۴۰۰"),
    dict(cap="مهندسی سیستم، چتری روی هر چهار شاخه", h=[9, 9, 6.5, 6.5], grow=[], ev=[], umbrella=True),
    dict(cap="گروه دیجیتال | سه سال آخر", h=[9, 9, 9, 6.5], grow=[2],
         ev=[(2, "ابزارهای مبتنی بر LLM و Agentها؛ مسئول بخش هوش مصنوعی")], yr="۱۴۰۲-۱۴۰۴"),
    dict(cap="گروه دیجیتال: ساختار و نرم‌افزار", h=[9, 9, 9, 9], grow=[3],
         ev=[(3, "فرآیندسازی؛ Confluence از صفر؛ معماری UNS؛ پیشنهاد ChirpStack؛ بخش تست")], yr="۱۴۰۵"),
    dict(end=True, cap="", h=[9, 9, 9, 9], grow=[], ev=[]),
]
