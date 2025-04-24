import base64
import io
import zipfile
from odoo.http import request, content_disposition

from odoo import http


class ProductImageDownload(http.Controller):
    """ This controller class contains the method of download the images """

    @http.route(['/download_images/<model("product.template"):product_id>'], type='http', auth="public", website=True)
    def download_product_images(self, product_id, **kwargs):
        """ This method checks the image is multiple of single if the multiple
         then it will ake a zip and download it to the system and if the single
         then it will download that single image only """
        product = request.env['product.template'].sudo().browse(product_id.id)
        image = product.image_1920
        multi_image = [img for img in product_id.product_template_image_ids]

        if not multi_image:
            # Single image download
            image_data = base64.b64decode(image)
            return request.make_response(image_data, [
                ('Content-Disposition', content_disposition(f"{product.name}"))
            ])
        # Multiple images → Create a ZIP file
        else:
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
                product_image_data = base64.b64decode(image)
                zipf.writestr(f"{product.name}_{1}", product_image_data)
                count = 1
                for img in multi_image:
                    img_data = base64.b64decode(img.image_1920)
                    count += 1
                    zipf.writestr(f"{product.name}_{count}", img_data)

            zip_buffer.seek(0)
            return request.make_response(zip_buffer.read(), [
                ('Content-Type', 'application/zip'),
                ('Content-Disposition', content_disposition(f"{product.name}_images.zip"))
            ])
