from fastapi import APIRouter, Response, Request, HTTPException

router = APIRouter(prefix="/process-xml", tags=["Process XML"])


@router.post("/")
async def process_xml(request: Request):
    try:
        body = await request.body()

        return Response(
            content=body.decode("utf-8"),
            media_type="application/xml"
        )
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
