import barcode
from barcode.writer import ImageWriter
from pathlib import Path


class BarcodeService:

    BARCODE_DIR = Path("media/barcodes")

    @classmethod
    def generate_barcode(cls, id_owner: str, model_id: int) -> tuple[str, str]:
        # id_owner
        # M - Member
        # V - Visitor
        # O - Ordinary visitor

        cls.BARCODE_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        code = f"{id_owner}-{model_id:013d}"

        filename = (
            cls.BARCODE_DIR / code
        )

        barcode_class = barcode.get_barcode_class(
            "code128"
        )

        barcode_instance = barcode_class(
            code,
            writer=ImageWriter()
        )

        barcode_instance.save(
            str(filename),
            options={
                "write_text": True,
                "module_width": 0.3,
                "module_height": 15,
                "font_size": 10,
                "text_distance": 5,
                "quiet_zone": 6
            }
        )

        return (
            code,
            f"media/barcodes/{code}.png"
        )
