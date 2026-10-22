"""
litigations data operations route v1
"""

from fastapi import APIRouter, Depends, HTTPException, status

from data.litigation_service import LitigationService
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/litigations",
    tags=["litigations"],
    responses={404: {"description": "Not found"}},
)


def get_litigation_service() -> LitigationService:
    """
    dependency to get the LitigationService instance.
    This allows for easy testing and mocking of the service.
    """
    return LitigationService()


@router.get("/")
async def fetch_litigations(
    repository: LitigationService = Depends(get_litigation_service),
):
    """
    retrieve all litigations from database (requires authentication)
    """
    logger.info("Fetching all litigations")

    try:
        litigations = repository.get_litigations()
        if litigations is None:
            logger.warning("No litigations found or database error")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No litigations found"
            )
        logger.info(f"Successfully fetched {len(litigations)} litigations")
        return {"data": litigations}
    except HTTPException:
        raise
    except Exception as e:  # pylint: disable=broad-except
        logger.error(f"Error fetching litigations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching litigations",
        ) from e


@router.get("/{litigation_id}")
async def fetch_litigation_by_id(
    litigation_id: str,
    repository: LitigationService = Depends(get_litigation_service),
):
    """
    retrieve a specific litigation by its ID from database (requires authentication)
    """
    logger.info(f"Fetching litigation with ID: {litigation_id}")

    try:
        litigation = repository.get_litigation_by_id(litigation_id)
        if litigation is None:
            logger.warning(f"Litigation with ID {litigation_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Litigation with ID {litigation_id} not found",
            )
        logger.info(f"Successfully fetched litigation with ID: {litigation_id}")
        return {"data": litigation}
    except HTTPException:
        raise
    except Exception as e:  # pylint: disable=broad-except
        logger.error(f"Error fetching litigation with ID {litigation_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching litigation with ID {litigation_id}",
        ) from e
