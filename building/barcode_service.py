import qrcode as qr
from pathlib import Path


class BarcodeService:

    BARCODE_DIR = Path("media/barcodes")

    @classmethod
    def generate_barcode(cls, id_owner: str, model_token: str) -> tuple[str, str]:
        # id_owner
        # M - Member
        # V - Visitor
        # O - Ordinary visitor

        cls.BARCODE_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        code = f"{id_owner}{model_token}"

        image_qrcode = qr.make(code)
        image_qrcode.save(f"{cls.BARCODE_DIR}/{code}.png")

        return (
            code,
            f"media/barcodes/{code}.png"
        )
