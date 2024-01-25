from typing import List, Union

from pydantic import BaseModel


class PartOfSpeech(BaseModel):
    value: str
    explanation: str


class Morphology(BaseModel):
    tags: list[str]
    explanation: Union[str, None]


class SyntacticalAnalysis(BaseModel):
    word: str
    pos: PartOfSpeech
    morphology: Union[Morphology, None]
    lemma: Union[str, None]
    dependency: Union[str, None]

    def stringify_lemma(self) -> str:
        return f' (from: {self.lemma})' if self.lemma else None

    def stringify_morphology(self) -> Union[str, None]:
        if self.morphology:
            if self.morphology.explanation:
                return self.morphology.explanation
            else:
                return ', '.join(self.morphology.tags)
        else:
            return None

    def stringify_dependency(self) -> Union[str, None]:
        # Only return something IF there is a dependency AND a the word is inflected in the first place
        return f' (refers to: {self.dependency})' if self.dependency and self.lemma else None

    def stringify(self) -> str:
        features: List[str] = []
        add_feature(features, self.stringify_lemma())
        add_feature(features, self.pos.explanation)
        add_feature(features, self.stringify_morphology())
        # add_feature(features, self.dependency)
        return '; '.join(features)


def add_feature(features: list[str], feature: Union[str, None]):
    if feature:
        features.append(feature)
