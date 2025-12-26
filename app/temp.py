@router.post("/address/{address_id}/make-default")
def make_default_address(
    address_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # unset old default
    db.query(Address).filter(
        Address.user_id == current_user.id,
        Address.is_default == True
    ).update({"is_default": False})

    # set new default
    address = db.query(Address).filter(
        Address.id == address_id,
        Address.user_id == current_user.id
    ).first()

    if not address:
        raise HTTPException(status_code=404)

    address.is_default = True
    db.commit()

    return RedirectResponse("/profile", status_code=302)
