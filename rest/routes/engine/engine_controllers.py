import uuid

from sqlalchemy import select, update

from rest.models.base_db.models import JSON_App, AppState
from fastapi import APIRouter, HTTPException, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from rest.database import get_async_session
from rest.models.engine.engine_model import EngineDocument, Configuration, engineSettings
from rest.kafka_producer import kafka_producer


router = APIRouter(
    prefix="/engine",
    tags=["Engine"])

@router.post("/")
async def create_engine_item(
    engine_item: EngineDocument,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        new_uuid = uuid.uuid4()

        new_app = JSON_App(
            UUID=new_uuid,
            kind=engine_item.kind,
            name=engine_item.name,
            version=engine_item.version,
            description=engine_item.description,
            state=AppState.NEW,
            json=engine_item.dict()
        )
        session.add(new_app)
        await session.commit()

        kafka_message = {"uuid": str(new_uuid), "kind": engine_item.name, "name": engine_item.name}
        await kafka_producer.send_message("quickstrt-event", str(new_uuid), kafka_message)

        return {"uuid": str(new_uuid)}

    except Exception as e:

        await session.rollback()
        raise HTTPException(status_code=500, detail=f"error to create engine file: {str(e)}")

@router.put("/{uuid}/configuration/")
async def update_engine_configuration(
    configuration: Configuration,
    uuid: uuid.UUID = Path(..., description="UUID of the item"),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        statement = select(JSON_App).where(JSON_App.UUID == uuid)
        app = await session.execute(statement)

        if not app:
            raise HTTPException(status_code=404, detail="Engine not found")

        app = app.scalar_one()

        app.json['configuration']['specification'] = configuration.specification.dict()
        app.json['configuration']['settings'] = configuration.settings.dict()

        await session.execute(
            update(JSON_App)
            .where(JSON_App.UUID == uuid)
            .values(json=app.json)
        )

        await session.commit()

        return {"message": f"Configuration updated successfully for UUID: {uuid}"}

    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update configuration: {str(e)}")

@router.put("/{uuid}/settings/")
async def update_engine_settings(
    settings: engineSettings,
    uuid: uuid.UUID = Path(..., description="UUID of the item"),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        statement = select(JSON_App).where(JSON_App.UUID == uuid)
        app = await session.execute(statement)

        if not app:
            raise HTTPException(status_code=404, detail="Engine not found")

        app = app.scalar_one()

        app.json['configuration']['settings'] = settings.dict()

        await session.execute(
            update(JSON_App)
            .where(JSON_App.UUID == uuid)
            .values(json=app.json)
        )

        await session.commit()

        return {"message": f"Configuration updated successfully for UUID: {uuid}"}

    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update configuration: {str(e)}")


@router.put("/{uuid}/state/")
async def update_engine_state(
    new_state: AppState,
    uuid: uuid.UUID = Path(..., description="UUID of the item"),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        app = await session.execute(
            select(JSON_App).where(JSON_App.UUID == uuid)
        )
        if not app:
            raise HTTPException(status_code=404, detail="Engine not found")

        app = app.scalar_one()
        app.state = new_state.value

        await session.commit()

        return {"message": f"State updated successfully for UUID: {uuid}"}

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update state: {str(e)}")

@router.delete("/{uuid}/")
async def delete_engine_item(
    uuid: uuid.UUID = Path(..., description="UUID of the item"),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        app = await session.execute(
            select(JSON_App).where(JSON_App.UUID == uuid)
        )

        if not app:
            raise HTTPException(status_code=404, detail=f"Engine not found")

        app = app.scalar_one()

        await session.delete(app)
        await session.commit()

        return {"message": f"Engine with UUID {uuid} deleted successfully"}

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete engine item: {str(e)}")


@router.get("/{uuid}")
async def read_engine_item(
    uuid: uuid.UUID = Path(..., description="UUID of the item"),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        app = await session.execute(
            select(JSON_App).where(JSON_App.UUID == uuid)
        )

        if not app:
            raise HTTPException(status_code=404, detail=f"Engine not found")

        app = app.scalar_one()


        return {
            "UUID": str(app.UUID),
            "kind": app.kind,
            "name": app.name,
            "version": app.version,
            "description": app.description,
            "state": app.state.value,
            "json": app.json
        }

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete engine item: {str(e)}")

@router.get("/{uuid}/state")
async def read_engine_state(
    uuid: uuid.UUID = Path(..., description="UUID of the item"),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        app = await session.execute(
            select(JSON_App).where(JSON_App.UUID == uuid)
        )

        if not app:
            raise HTTPException(status_code=404, detail=f"Engine not found")

        app = app.scalar_one()


        return {
            "state": app.state.value
        }

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete engine item: {str(e)}")
