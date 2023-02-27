from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

word_components = db.Table(
    "word_components",
    db.Column("word_id", db.Integer, db.ForeignKey("word.id"), primary_key=True),
    db.Column("kanji_id", db.Integer, db.ForeignKey("kanji.id"), primary_key=True)    
)

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    written = db.Column(db.String(32))
    reading = db.Column(db.String(64))
    meaning = db.Column(db.String(256))
    
    kanji_list = db.relationship("Kanji", secondary=word_components, back_populates="words")

    def serialize(self, short_form=False):
        doc = {
            "written": self.written,
            "reading": self.reading,
            "meaning": self.meaning
        }
        if not short_form:
            result = []
            for kanji in self.kanji_list:
                result.append({
                    "kanji": kanji.kanji,
                    "meaning": kanji.meaning
                })
            doc["kanji_list"] = result
        return doc

class Kanji(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kanji = db.Column(db.String(8))
    meaning = db.Column(db.String(256))
    kunyomi = db.Column(db.String(256), nullable=True)
    onyomi = db.Column(db.String(256), nullable=True)
    strokes = db.Column(db.Integer)
    
    words = db.relationship("Word", secondary=word_components, back_populates="kanji_list")

    def serialize(self, short_form=False):
        doc = {
            "kanji": self.kanji,
            "meaning": self.meaning
        }
        if not short_form:
            doc["kunyomi"] = self.kunyomi
            doc["onyomi"] = self.onyomi
            doc["strokes"] = self.strokes
        return doc