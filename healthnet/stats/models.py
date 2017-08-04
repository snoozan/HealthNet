from collections import Counter

from django.db import models

import datetime

from med_information.models.prescription import Prescription
from med_information.models.record import Record
from users.models import Hospital, Patient


class Statistics(models.Model):
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def number_admitted_patients(self):
        return len(Patient.objects.filter(hospital=self.hospital.id, admitted=True))

    def avg_num_visits_patient(self):
        """
        returns the average number of visits per patient
        """
        patients = Patient.objects.all()
        count = 0
        for patient in patients:
            count += len(Record.objects.filter(patient_id=patient.id))
        return count/len(patients)


    def avg_visits_length(self):
        records = Record.objects.filter(discharged=True)
        patient_visit = []
        for record in records:
            patient_visit.append(record.endDate - record.startDate)
        return sum(patient_visit, datetime.timedelta()) / (len(patient_visit)+1)

    def get_popular_prescriptions(self):
        names = [script.title for script in Prescription.objects.all()]
        return Counter(names).most_common(1)

    def get_most_common_reason(self):
        reasons = [record.reason for record in Record.objects.all()]
        return Counter(reasons).most_common(1)
