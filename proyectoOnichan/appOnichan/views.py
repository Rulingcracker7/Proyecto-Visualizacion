from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.http import require_POST
import json

def index(request):
    return render(request, 'pagina1.html')

def pagina2(request):
    return render(request, 'pagina2.html')

def pagina3(request):
    return render(request, 'pagina3.html')


def pagina4(request):
    """Dashboard view — renderiza la plantilla de dashboard con datos de ejemplo.
    El frontend contiene scripts que usan Chart.js; aquí solo pasamos ejemplos mínimos.
    """
    # Ejemplo de contexto con KPIs (en desarrollo serán reemplazados por datos reales)
    context = {
        'kpi_today': 12,
        'kpi_pending': 5,
        'kpi_revenue_7d': 125000,
        'orders_by_day': [5,8,12,9,10,7,11],
        'products_top': [
            {'label': 'Producto A', 'value': 42},
            {'label': 'Producto B', 'value': 31},
            {'label': 'Producto C', 'value': 25},
            {'label': 'Producto D', 'value': 18},
            {'label': 'Producto E', 'value': 12},
        ],
    }
    # Serializar a JSON para el template JS
    context['orders_by_day_json'] = json.dumps(context['orders_by_day'])
    context['products_top_json'] = json.dumps(context['products_top'])
    # Si se solicita un producto específico via GET ?product=Label, preparar datos de detalle
    selected = request.GET.get('product')
    if selected:
        # Generar datos de ejemplo para el producto seleccionado (p. ej. ventas por mes)
        product_series = {
            'label': selected,
            'months': ['Ago','Sep','Oct','Nov','Dic','Ene','Feb','Mar','Abr','May','Jun','Jul'],
            'values': [randval for randval in [1200,1500,1700,900,800,1300,1600,1400,1800,1900,2100,2300]]
        }
        # Si quieres datos dinámicos, reemplaza por consultas a la base de datos
        context['selected_product'] = selected
        context['product_detail_json'] = json.dumps(product_series)

    # Serializar a JSON para el template JS
    context['orders_by_day_json'] = json.dumps(context['orders_by_day'])
    context['products_top_json'] = json.dumps(context['products_top'])
    return render(request, 'pagina4.html', context)


def api_orders(request):
    """Return a small sample JSON payload of orders for frontend JS to consume.
    This is a minimal implementation so templates that expect AJAX can call it.
    """
    # In a real app replace with ORM queries. We'll return a static sample.
    sample = [
        {"id": 1001, "cliente": "Valeria", "estado": "Pendiente", "total": 12000, "metodo": "Tarjeta", "fecha": "2025-11-03T10:00:00"},
        {"id": 1002, "cliente": "Benjamín", "estado": "Despachado", "total": 4500, "metodo": "Efectivo", "fecha": "2025-11-02T15:30:00"},
    ]
    return JsonResponse({"orders": sample})


@require_POST
def api_order_update(request, order_id):
    """Accepts JSON {"estado": "NuevoEstado"} and returns updated order.
    This is a stub: no persistence, just echoes back.
    """
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except Exception:
        return HttpResponseBadRequest('Invalid JSON')
    estado = payload.get('estado')
    if not estado:
        return HttpResponseBadRequest('Missing estado')
    # Echo response
    return JsonResponse({"order": {"id": order_id, "estado": estado}})


@require_POST
def contact(request):
    # Minimal handler for contact form: accept POST and return simple response
    name = request.POST.get('name') or request.POST.get('nombre')
    message = request.POST.get('message') or request.POST.get('mensaje')
    if not message:
        return HttpResponseBadRequest('Falta mensaje')
    # In real app: save or send email
    return JsonResponse({"ok": True, "msg": "Mensaje recibido"})


@require_POST
def checkout(request):
    # Minimal checkout handler: accept POST and return success
    # In real app validate cart, payment, create Order instance, etc.
    return JsonResponse({"ok": True, "msg": "Checkout simulado completado"})


def product_detail(request, product_label):
    """Subvista que muestra un gráfico detallado para un producto.
    En desarrollo devolvemos datos de ejemplo distintos según la etiqueta.
    """
    # Crear datos de ejemplo que dependan del product_label
    base = sum(ord(c) for c in product_label) % 1000
    months = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
    values = [base + (i * (len(product_label) % 7 + 1) * 100) % 2000 + (i*50) for i in range(len(months))]
    detail = {
        'label': product_label,
        'months': months,
        'values': values,
    }
    # Prepare month/value pairs for template iteration (avoid needing a 'zip' filter)
    month_values = list(zip(months, values))
    return render(request, 'product_detail.html', {
        'product': detail,
        'product_json': json.dumps(detail),
        'product_month_values': month_values,
    })