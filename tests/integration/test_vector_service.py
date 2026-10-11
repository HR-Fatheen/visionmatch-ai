from dotenv import load_dotenv

from app.database import SessionLocal
from app.models.image import Image
from app.models.image_vector import ImageVector
from app.services.vector_service import save_image_vector


load_dotenv()

db = SessionLocal()

try:
    image = Image(
        filename="vector-test.jpg",
        filepath="data/images/vector-test.jpg",
    )

    db.add(image)
    db.commit()
    db.refresh(image)

    vector = [0.001] * 3072

    saved_vector = save_image_vector(
        db=db,
        image_id=image.id,
        vector=vector,
    )

    print("Image ID:", image.id)
    print("Vector ID:", saved_vector.id)
    print("Vector dimensions:", len(saved_vector.embedding))

    assert saved_vector.image_id == image.id
    assert len(saved_vector.embedding) == 3072

    stored_vector = db.query(ImageVector).filter(
        ImageVector.image_id == image.id
    ).first()

    assert stored_vector is not None
    assert len(stored_vector.embedding) == 3072

    print("Vector storage test: PASSED")

finally:
    db.close()