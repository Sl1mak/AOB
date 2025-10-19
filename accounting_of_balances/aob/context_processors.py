def username_context(request):
    username = request.session.get("username")
    return {"username": username}