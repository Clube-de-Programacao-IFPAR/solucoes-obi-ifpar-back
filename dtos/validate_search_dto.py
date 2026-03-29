class ValidateSearchDTO:
    def __init__(
            self, 
            year: str | None = None, 
            phase: str | None = None, 
            level: str | None = None, 
            problem: str | None = None
        ):
            self.year = year
            self.phase = phase
            self.level = level
            self.problem = problem

    def validate(self):
        if self.year and not self.year.isdigit():
            return {"error": "Invalid year format"}, 400

        if self.phase and self.phase not in ("c", "1", "2", "3"):
            return {"error": "Invalid phase format"}, 400

        if self.level and self.level not in ("j", "1", "2", "s", "u"):
            return {"error": "Invalid level format"}, 400

        return None
