from django.db import models

class ContactMessage(models.Model):
    SERVICE_CHOICES = [
        ('maison', 'Maison / Impeccable'),
        ('privilège', 'Matin / Privilège'),
        ('Courses', 'Courses & Quotidien'),
        ('prête', 'maison / prête'),
        ('reception','Autre /  besoin'),
        ('voyage','Retour / Voyage'),
        ('demande','Autre / demande / personnalisée')
    ]

    first_name = models.CharField(max_length=100, verbose_name="Prénom")
    last_name = models.CharField(max_length=100, verbose_name="Nom")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Téléphone", blank=True, null=True)
    service = models.CharField(
        max_length=50, 
        choices=SERVICE_CHOICES, 
        default='autre', 
        verbose_name="Prestation souhaitée"
    )
    message = models.TextField(verbose_name="Message / Description des besoins")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'envoi")
    is_read = models.BooleanField(default=False, verbose_name="Lu")

    class Meta:
        verbose_name = "Message de Contact"
        verbose_name_plural = "Messages de Contact"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_service_display()} ({self.created_at.strftime('%d/%m/%Y')})"

