
"""
Framework Services Constant Module
"""


#   CLEARANCE LEVELS
HIGH: int = 3
MEDIUM: int = 2
MED: int = 2
LOW: int = 1
ANY: int = 0


#   SERVICE LOG MESSAGES
SLM_F_001: str = "Appended '{call}' call to framework services"
SLM_F_002: str = "Successfully added {cls} to services whitelist"
SLM_F_003: str = "Failed to whitelist '{cls}' because {requestor} " \
                 "class is not authorized to do so"
SLM_F_004: str = "Failed to authorize '{cls}' because {requestor} " \
                 "class is not authorized to do so"
SLM_F_005: str = "Provided {cls} with service administrative privileges"
SLM_F_006: str = "No services available for '{requestor}'"
SLM_F_007: str
SLM_F_008: str
SLM_F_009: str
SLM_F_010: str
SLM_F_011: str
