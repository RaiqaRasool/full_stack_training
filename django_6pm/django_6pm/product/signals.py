from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse

from product.models import ProductColorSize, SkuSubscription
from product.tasks import send_html_email


@receiver(pre_save, sender=ProductColorSize)
def send_email_on_stock_change(sender, instance, **kwargs):
    previous_instance = ProductColorSize.objects.select_related("product", "color").get(pk=instance.pk)
    current_site = Site.objects.get_current()
    product_url = reverse("product", args=[previous_instance.product.retailer_sku])
    absolute_url = f"{current_site.domain}{product_url}"
    if (previous_instance.is_in_stock != instance.is_in_stock) and (instance.is_in_stock):
        print(f"Sending email for product {previous_instance.product.name}")
        skusubscriptions = previous_instance.subscriptions.all()
        subject = f"{previous_instance.product.name} Sku back in stock!!"
        template_name = "product/sku_in_stock_email.html"
        context = {
            "product_name": previous_instance.product.name,
            "product_url": absolute_url,
            "sku_color": previous_instance.color.color,
            "sku_size": previous_instance.size,
        }
        receipients_list = [skusubscription.email for skusubscription in skusubscriptions]
        print("Sending email: ", context)
        send_html_email.delay(subject, template_name, context, receipients_list)
