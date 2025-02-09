import uuid

from sqlalchemy import select, update

from rest.models.base_db.models import JSON_App, AppState
from fastapi import APIRouter, HTTPException, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from rest.database import get_async_session
from rest.models.test.test_model import TestDocument, Configuration, testSettings
from rest.kafka_producer import kafka_producer


router = APIRouter(
    prefix="/test",
    tags=["Test"])

@router.post("/")
async def create_test_item(
    test_item: TestDocument,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        new_uuid = uuid.uuid4()

        new_app = JSON_App(
            UUID=new_uuid,
            kind=test_item.kind,
            name=test_item.name,
            version=test_item.version,
            description=test_item.description,
            state=AppState.NEW,
            json=test_item.dict()
        )
        session.add(new_app)
        await session.commit()
        try:
            kafka_message = {"uuid": str(new_uuid), "kind": test_item.name, "name": test_item.name}
            await kafka_producer.send_message("quickstrt-event", str(new_uuid), kafka_message)
        except Exception as e:
            print(e)

        return {"uuid": str(new_uuid)}

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"error to create test file: {str(e)}")

@router.put("/{uuid}/configuration/")
async def update_test_configuration(
    configuration: Configuration,
    uuid: uuid.UUID = Path(..., description="UUID of the item"),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        app = await session.execute(
            select(JSON_App).where(JSON_App.UUID == uuid, JSON_App.kind == "test")
        )

        app = app.scalars().first()

        if not app:
            raise HTTPException(status_code=404, detail="test item not found")

        old_config = app.json['configuration']
        app.json['configuration']['specification'] = configuration.specification.dict()
        app.json['configuration']['settings'] = configuration.settings.dict()
        new_config = app.json['configuration']

        await session.execute(
            update(JSON_App)
            .where(JSON_App.UUID == uuid)
            .values(json=app.json)
        )

        await session.commit()

        try:
            kafka_message = {"uuid": str(app.UUID), "old_config": old_config, "new_config": new_config}
            await kafka_producer.send_message("quickstrt-event", str(app.UUID), kafka_message)
        except Exception as e:
            print(e)

        return {"message": f"Configuration updated successfully for UUID: {uuid}"}

    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update configuration: {str(e)}")

@router.put("/{uuid}/settings/")
async def update_test_settings(
    settings: testSettings,
    uuid: uuid.UUID = Path(..., description="UUID of the item"),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        app = await session.execute(
            select(JSON_App).where(JSON_App.UUID == uuid, JSON_App.kind == "test")
        )

        app = app.scalars().first()

        if not app:
            raise HTTPException(status_code=404, detail="test item not found")

        old_settings = app.json['configuration']['settings']
        app.json['configuration']['settings'] = settings.dict()
        new_settings = app.json['configuration']['settings']

        await session.execute(
            update(JSON_App)
            .where(JSON_App.UUID == uuid)
            .values(json=app.json)
        )

        await session.commit()

        try:
            kafka_message = {"uuid": str(app.UUID), "old_settings": old_settings, "new_settings": new_settings}
            await kafka_producer.send_message("quickstrt-event", str(app.UUID), kafka_message)
        except Exception as e:
            print(e)

        return {"message": f"Configuration updated successfully for UUID: {uuid}"}

    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update settings: {str(e)}")


@router.put("/{uuid}/state/")
async def update_test_state(
    new_state: AppState,
    uuid: uuid.UUID = Path(..., description="UUID of the item"),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        app = await session.execute(
            select(JSON_App).where(JSON_App.UUID == uuid, JSON_App.kind == "test")
        )

        app = app.scalars().first()

        if not app:
            raise HTTPException(status_code=404, detail="test item not found")


        old_state = app.state
        app.state = new_state.value

        await session.commit()

        try:
            kafka_message = {"uuid": str(app.UUID), "old_state": str(old_state), "new_state": str(new_state.value)}
            await kafka_producer.send_message("quickstrt-event", str(app.UUID), kafka_message)
        except Exception as e:
            print(e)

        return {"message": f"State updated successfully for UUID: {uuid}"}

    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update state: {str(e)}")

@router.delete("/{uuid}/")
async def delete_test_item(
    uuid: uuid.UUID = Path(..., description="UUID of the item"),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        app = await session.execute(
            select(JSON_App).where(JSON_App.UUID == uuid, JSON_App.kind == "test")
        )

        app = app.scalars().first()

        if not app:
            raise HTTPException(status_code=404, detail="test item not found")

        await session.delete(app)
        await session.commit()

        try:
            kafka_message = {"uuid": str(uuid), "deleted": True}
            await kafka_producer.send_message("quickstrt-event", str(uuid), kafka_message)
        except Exception as e:
            print(e)

        return {"message": f"Test with UUID {uuid} deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete test item: {str(e)}")


@router.get("/{uuid}")
async def read_test_item(
    uuid: uuid.UUID = Path(..., description="UUID of the item"),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        app = await session.execute(
            select(JSON_App).where(JSON_App.UUID == uuid, JSON_App.kind == "test")
        )

        app = app.scalars().first()

        if not app:
            raise HTTPException(status_code=404, detail="test item not found")

        try:
            kafka_message = {"uuid": str(uuid), "get": True}
            await kafka_producer.send_message("quickstrt-event", str(app.UUID), kafka_message)
        except Exception as e:
            print(e)

        return {
            "UUID": str(app.UUID),
            "kind": app.kind,
            "name": app.name,
            "version": app.version,
            "description": app.description,
            "state": app.state.value,
            "json": app.json
        }

    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to get test item: {str(e)}")

@router.get("/{uuid}/state")
async def read_test_state(
    uuid: uuid.UUID = Path(..., description="UUID of the item"),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        app = await session.execute(
            select(JSON_App).where(JSON_App.UUID == uuid, JSON_App.kind == "test")
        )

        app = app.scalars().first()

        if not app:
            raise HTTPException(status_code=404, detail="test item not found")


        try:
            kafka_message = {"uuid": str(app.UUID), "get_state": True}
            await kafka_producer.send_message("quickstrt-event", str(app.UUID), kafka_message)
        except Exception as e:
            print(e)

        return {
            "state": app.state.value
        }

    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to get state test item: {str(e)}")
