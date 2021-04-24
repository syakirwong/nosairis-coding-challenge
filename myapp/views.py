from django.shortcuts import render
from myapp.models import DataTerminal, AlertReport
from datetime import datetime
import time

# Create your views here.
def home_view(request, *args, **kwargs):
    data =  DataTerminal.objects.all()
    S1_data = DataTerminal.objects.raw('SELECT * FROM data_terminal WHERE SW = "S1"')[:361]
    S2_data = DataTerminal.objects.raw('SELECT * FROM data_terminal WHERE SW = "S2"')[:361]
    S3_data = DataTerminal.objects.raw('SELECT * FROM data_terminal WHERE SW = "S3"')[:361]
    S1_labels = []
    S2_labels = []
    S3_labels = []
    S1_status = []
    S2_status = []
    S3_status = []

    for d in data:
        if d.T1 == 0 and d.T2 == 0 and d.T3 == 0 and d.T4 == 0 and d.T5 == 0:
            d.status = 0
            d.save()
            alert_report, created = AlertReport.objects.update_or_create(
                data_id = d.id,
                defaults = {
                    "data_id" : d.id, "SW" :d.SW, "alert_datetime" : d.TS,
                    "email_alert_datetime" : int(time.time())
                }
            )
        else:
            d.status = 1
            d.save()

    for d in S1_data:
        S1_labels.append(d.TS)
        S1_status.append(d.status)

    for d in S2_data:
        S2_labels.append(d.TS)
        S2_status.append(d.status)

    for d in S3_data:
        S3_labels.append(d.TS)
        S3_status.append(d.status)

    return render(request, "charts.html",
    { 'S1_data' :  S1_status , 'S1_labels': S1_labels,
      'S2_data' :  S2_status , 'S2_labels': S2_labels,
      'S3_data' :  S3_status , 'S3_labels': S3_labels })

def alert_report_view(request, *args, **kwargs):
    reports = AlertReport.objects.all()
    data = []
    for item in reports:
        data.append({
            'id' : item.id,
            'SW' : item.SW,
            'alert_type' : item.alert_type,
            'alert_datetime': datetime.fromtimestamp(item.alert_datetime),
            'email_alert_datetime': datetime.fromtimestamp(item.email_alert_datetime)})

    return render(request, "alert-report.html", {'data': data} )