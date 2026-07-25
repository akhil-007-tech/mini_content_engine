
from .models import Job
from .services import generate_prompt


def process_job(job_id):

    job = Job.objects.get(id=job_id)

    try:
        job.status = "PROCESSING"
        job.save()

        prompt = generate_prompt(
            job.product_name,
            job.description,
        )

        job.generated_prompt = prompt

        # Mock image URL
        job.generated_image_url = "https://picsum.photos/1024"

        job.status = "COMPLETED"

    except Exception as e:
        job.status = "FAILED"
        job.generated_prompt = str(e)

    job.save()