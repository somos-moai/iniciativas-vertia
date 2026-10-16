"""Application-specific demo identities and explicit capability policy (never SSO)."""

ROLE_CAPABILITIES = {
    "regional": ["read_all", "manage_records", "approve", "configure", "manage_credits"],
    "superadmin": ["read_all", "manage_records", "approve", "configure", "manage_credits", "manage_users"],
    "manager": ["read_country", "manage_records", "approve"],
    "executive": ["read_portfolio", "manage_records"],
    "legal": ["read_country", "manage_records", "approve"],
    "viewer": ["read_country"],
    "ia_lead": ["read_all", "configure_ai"],
    "innovation_admin": ["read_all", "configure_clm"],
}

def capabilities(user):
    return ROLE_CAPABILITIES.get(user["role"], [])

def supports(user, application):
    return application in user.get("apps", ["prospectador", "contratos"])

def all_countries(user):
    return "read_all" in capabilities(user)

def editable(user):
    return "manage_records" in capabilities(user)

def profiles(users, application):
    return [{**u, "capabilities": capabilities(u)} for u in users if supports(u, application)]
