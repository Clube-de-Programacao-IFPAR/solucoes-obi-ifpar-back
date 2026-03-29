class ValidateQuestionDTO:
    def __init__(
        self,
        year: str | None = None,
        phase: str | None = None,
        level: str | None = None,
        name: str | None = None,
        filename: str | None = None,
        file: str | None = None
    ):
        self.year = year
        self.phase = phase
        self.level = level
        self.name = name
        self.filename = filename
        self.file = file

    def validate(self):
        if not self.year or not self.year.isdigit():
            return {"error": "Invalid year"}, 400

        if not self.phase or self.phase not in ("c", "1", "2", "3"):
            return {"error": "Invalid phase"}, 400

        if not self.level or self.level not in ("j", "1", "2", "s", "u"):
            return {"error": "Invalid level"}, 400

        if not self.name:
            return {"error": "Missing problem name"}, 400

        if not self.filename:
            return {"error": "Missing filename"}, 400

        if not self.file:
            return {"error": "Missing file content"}, 400

        return None
