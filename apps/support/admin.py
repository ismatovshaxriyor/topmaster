"""Admin registration for the help center + support chat.

The support chat is operated entirely from here: open a thread to read the
conversation (live, auto-refreshing), type a reply in the "Javob" box and save —
the reply is delivered to the user instantly (WebSocket + push + in-app
notification).
"""
from django import forms
from django.contrib import admin
from django.db.models import Case, IntegerField, Value, When
from django.http import JsonResponse
from django.urls import path, reverse
from django.utils import timezone
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe

from apps.support import services
from apps.support.models import Faq, FaqTopic, SupportMessage, SupportThread


class FaqInline(admin.TabularInline):
    model = Faq
    extra = 1
    fields = ("question", "answer", "order")


@admin.register(FaqTopic)
class FaqTopicAdmin(admin.ModelAdmin):
    list_display = ("label", "key", "icon", "order")
    list_editable = ("order",)
    search_fields = ("label", "key")
    prepopulated_fields = {"key": ("label",)}
    inlines = (FaqInline,)


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ("question", "topic", "order")
    list_filter = ("topic",)
    search_fields = ("question", "answer")


# ── Support chat ──────────────────────────────────────────────────
class StatusButtonsWidget(forms.RadioSelect):
    """Render a choice field as a row of coloured pill buttons (a radio group).

    Pure CSS — clicking a pill selects it (native radio) and it lights up in the
    status colour; submits normally on Save.
    """

    _COLORS = {"open": "#2E6488", "pending": "#E0A52E", "resolved": "#1F8A5B", "closed": "#807E74"}
    _CSS = mark_safe(
        "<style>"
        ".tm-status-group{display:flex;flex-wrap:wrap;gap:8px;align-items:center}"
        ".tm-status-group input[type=radio]{position:absolute;opacity:0;width:0;height:0}"
        ".tm-status-group label{display:inline-block;padding:7px 18px;border-radius:999px;"
        "border:1.5px solid #3a4a5a;background:#16202b;color:#9fc3da;cursor:pointer;"
        "font-weight:600;font-size:13px;margin:0;transition:all .15s}"
        ".tm-status-group label:hover{border-color:#4E82A6}"
        ".tm-status-group input[type=radio]:checked+label{background:var(--c);border-color:var(--c);color:#fff}"
        ".tm-status-group input[type=radio]:focus+label{outline:2px solid #4E82A6;outline-offset:1px}"
        "</style>"
    )

    def render(self, name, value, attrs=None, renderer=None):
        value = "" if value is None else str(value)
        buttons = format_html_join(
            "",
            '<input type="radio" name="{}" id="{}" value="{}"{}>'
            '<label for="{}" style="--c:{}">{}</label>',
            (
                (
                    name,
                    f"id_{name}_{i}",
                    str(val),
                    mark_safe(" checked") if str(val) == value else mark_safe(""),
                    f"id_{name}_{i}",
                    self._COLORS.get(str(val), "#807E74"),
                    label,
                )
                for i, (val, label) in enumerate(self.choices)
            ),
        )
        return format_html(
            '{}<div class="tm-status-group">{}</div>', self._CSS, buttons
        )


class SupportThreadForm(forms.ModelForm):
    reply = forms.CharField(
        label="Javob yozish",
        required=False,
        widget=forms.Textarea(
            attrs={"rows": 4, "placeholder": "Foydalanuvchiga javob yozing…  (Ctrl/⌘+Enter — yuborish)",
                   "style": "width:90%;max-width:680px"}
        ),
        help_text="Saqlaganda javob foydalanuvchiga darhol yuboriladi.",
    )

    class Meta:
        model = SupportThread
        fields = ("subject", "status")
        widgets = {"status": StatusButtonsWidget}


# Client-side chat widget: renders bubbles from JSON, polls for new messages,
# auto-scrolls, adds quick replies + Ctrl/⌘+Enter. URL is injected per thread.
_CHAT_SCRIPT = r"""
<script>(function(){
  function init(){
  var box=document.getElementById('tm-chat'); if(!box) return;
  var URL='__URL__', last=0, first=true;
  function esc(s){var d=document.createElement('div');d.textContent=s||'';return d.innerHTML;}
  function bubble(m){
    var mine=m.is_staff, side=mine?'flex-end':'flex-start',
        bg=mine?'#1B4965':'#2b3a4a', av=mine?'#F4A259':'#4E82A6',
        ini=(m.name||'?').trim().charAt(0).toUpperCase(),
        tick=mine?(m.read?' ✓✓':' ✓'):'';
    var avatar='<div style="width:28px;height:28px;border-radius:50%;flex:none;background:'+av+';color:#0d2230;'
      +'display:flex;align-items:center;justify-content:center;font-weight:700;font-size:12px">'+esc(ini)+'</div>';
    var b='<div style="max-width:70%;padding:8px 12px;border-radius:14px;background:'+bg+';color:#eaf2f8;'
      +'box-shadow:0 1px 2px rgba(0,0,0,.35)">'
      +'<div style="font-size:11px;opacity:.65;margin-bottom:3px">'+esc(m.name)+' · '+esc(m.time)+tick+'</div>'
      +'<div style="white-space:pre-wrap;line-height:1.45">'+esc(m.text)+'</div></div>';
    return '<div style="display:flex;gap:8px;align-items:flex-end;justify-content:'+side+';margin:8px 0">'
      +(mine?(b+avatar):(avatar+b))+'</div>';
  }
  function nearBottom(){return box.scrollHeight-box.scrollTop-box.clientHeight<90;}
  function load(){
    fetch(URL+'?after='+last,{credentials:'same-origin'}).then(function(r){return r.json();}).then(function(d){
      var msgs=d.messages||[];
      if(first){ box.innerHTML=''; if(!msgs.length){box.innerHTML='<em style="opacity:.6">Hali xabar yoʻq.</em>';} }
      if(msgs.length){
        var stick=first||nearBottom();
        msgs.forEach(function(m){box.insertAdjacentHTML('beforeend',bubble(m)); if(m.id>last)last=m.id;});
        if(stick) box.scrollTop=box.scrollHeight;
      }
      first=false;
    }).catch(function(){});
  }
  load(); setInterval(load,5000);
  var ta=document.getElementById('id_reply');
  if(ta){
    ta.addEventListener('keydown',function(e){
      if((e.ctrlKey||e.metaKey)&&e.key==='Enter'){var f=ta.closest('form');
        if(f){(f.querySelector('input[name=_continue]')||f.querySelector('input[name=_save]')).click();}}
    });
    var canned=['Assalomu alaykum! Sizga qanday yordam bera olaman?',
      'Murojaatingiz uchun rahmat, tez orada hal qilamiz.',
      'Buyurtmangiz koʻrib chiqilmoqda.',
      'Yana savolingiz boʻlsa, bemalol yozing.'];
    var bar=document.createElement('div'); bar.style.cssText='margin:8px 0 4px;display:flex;gap:6px;flex-wrap:wrap';
    canned.forEach(function(t){var b=document.createElement('button'); b.type='button'; b.title=t;
      b.textContent=t.length>30?t.slice(0,30)+'…':t;
      b.style.cssText='font-size:12px;padding:4px 11px;border-radius:999px;border:1px solid #2E6488;'
        +'background:#16202b;color:#9fc3da;cursor:pointer';
      b.onclick=function(){ta.value=ta.value?(ta.value.replace(/\s+$/,'')+' '+t):t; ta.focus();};
      bar.appendChild(b);});
    ta.parentNode.insertBefore(bar,ta);
  }
  }
  if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',init);}else{init();}
})();</script>
"""


@admin.register(SupportThread)
class SupportThreadAdmin(admin.ModelAdmin):
    form = SupportThreadForm
    list_display = (
        "id", "user", "subject_display", "status_badge",
        "staff_unread", "updated_at",
    )
    list_filter = ("status",)
    search_fields = ("user__email", "user__full_name", "subject", "messages__text")
    readonly_fields = ("user", "transcript")
    fields = (
        "user", "subject", "status",
        "transcript", "reply",
    )
    actions = ("mark_resolved", "mark_closed")

    # ---- default ordering: active threads (open, then pending) on top,
    #      resolved/closed at the bottom; unread-from-user floats up ----
    _STATUS_PRIORITY = Case(
        When(status=SupportThread.Status.OPEN, then=Value(0)),
        When(status=SupportThread.Status.PENDING, then=Value(1)),
        When(status=SupportThread.Status.RESOLVED, then=Value(2)),
        default=Value(3),
        output_field=IntegerField(),
    )

    def get_queryset(self, request):
        # Annotate BEFORE ordering so get_ordering can sort by `_priority`.
        qs = self.model._default_manager.get_queryset().annotate(
            _priority=self._STATUS_PRIORITY
        )
        ordering = self.get_ordering(request)
        return qs.order_by(*ordering) if ordering else qs

    def get_ordering(self, request):
        return ("_priority", "-staff_unread", "-updated_at")

    # ---- custom JSON endpoint for the live chat widget ----
    def get_urls(self):
        custom = [
            path(
                "<int:thread_id>/chat-messages/",
                self.admin_site.admin_view(self.chat_messages_json),
                name="support_supportthread_chat_json",
            ),
        ]
        return custom + super().get_urls()

    def chat_messages_json(self, request, thread_id):
        after = request.GET.get("after") or 0
        try:
            after = int(after)
        except (TypeError, ValueError):
            after = 0
        qs = (
            SupportMessage.objects.filter(thread_id=thread_id, id__gt=after)
            .select_related("sender")
            .order_by("id")
        )
        data = [
            {
                "id": m.id,
                "is_staff": m.is_staff,
                "text": m.text,
                "name": "Support" if m.is_staff
                else (m.sender.full_name if m.sender else "Foydalanuvchi"),
                "time": timezone.localtime(m.created_at).strftime("%d-%m %H:%M"),
                "read": bool(m.read_at),
            }
            for m in qs
        ]
        return JsonResponse({"messages": data})

    @admin.display(description="Mavzu")
    def subject_display(self, obj):
        return obj.subject or "(mavzusiz)"

    @admin.display(description="Holat")
    def status_badge(self, obj):
        colors = {"open": "#2E6488", "pending": "#E0A52E", "resolved": "#1F8A5B", "closed": "#807E74"}
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 9px;border-radius:999px;'
            'font-size:12px;font-weight:600">{}</span>',
            colors.get(obj.status, "#807E74"), obj.get_status_display(),
        )

    @admin.display(description="Suhbat")
    def transcript(self, obj):
        if obj.pk is None:
            return "—"
        url = reverse("admin:support_supportthread_chat_json", args=[obj.pk])
        container = (
            '<div id="tm-chat" style="max-width:700px;height:440px;overflow-y:auto;'
            'padding:12px 14px;background:#0f1722;border:1px solid #243446;border-radius:12px">'
            '<em style="opacity:.6;color:#9fc3da">Yuklanmoqda…</em></div>'
        )
        return mark_safe(container + _CHAT_SCRIPT.replace("__URL__", url))

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        reply = (form.cleaned_data.get("reply") or "").strip()
        if reply:
            message = SupportMessage.objects.create(
                thread=obj, sender=request.user, is_staff=True, text=reply,
            )
            services.register_staff_reply(message)  # delivers to the user live

    def change_view(self, request, object_id, form_url="", extra_context=None):
        # Opening a thread = staff has seen the user's messages.
        thread = SupportThread.objects.filter(pk=object_id).first()
        if thread and thread.staff_unread:
            thread.staff_unread = 0
            thread.save(update_fields=["staff_unread", "updated_at"])
        return super().change_view(request, object_id, form_url, extra_context)

    @admin.action(description="Hal qilindi deb belgilash")
    def mark_resolved(self, request, queryset):
        queryset.update(status=SupportThread.Status.RESOLVED)

    @admin.action(description="Yopish")
    def mark_closed(self, request, queryset):
        queryset.update(status=SupportThread.Status.CLOSED)


@admin.register(SupportMessage)
class SupportMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "thread", "sender", "is_staff", "short_text", "created_at")
    list_filter = ("is_staff",)
    search_fields = ("text", "thread__user__email")
    readonly_fields = ("thread", "sender", "is_staff", "text", "attachment", "read_at", "created_at")

    @admin.display(description="Matn")
    def short_text(self, obj):
        return (obj.text or "")[:60]
