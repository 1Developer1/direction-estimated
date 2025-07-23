
from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config


class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"


class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image],Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"


class KeepSideFalse(Config):
    name: Literal["False"] = "False"
    value: Literal[False] = False
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Disable"


class KeepSideTrue(Config):
    name: Literal["True"] = "True"
    value: Literal[True] = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Enable"


class KeepSideBBox(Config):
    """
        Rotate image without catting off sides.
    """
    name: Literal["KeepSide"] = "KeepSide"
    value: Union[KeepSideTrue, KeepSideFalse]#birden fazla değer alabilmesini istiyorsak union kullanıyoruz.
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"#dependedDropdownlist olarak yazarsak seçtiğimizde seçtiğimiz şeyler için ayrıca parametre seçebiliriz.

    class Config:
        title = "Keep Sides"


class Degree(Config):
    #burada açıklama satırı olarak yazılan metin arayüzde gözükecektir.
    """
        Positive angles specify counterclockwise rotation while negative angles indicate clockwise rotation.
    """
    name: Literal["Degree"] = "Degree"#executorda parametreleri çekmek için kullandığımız namedir.
    value: int = Field(ge=-359.0, le=359.0,default=0)#burada ise sınırları belirtebiliriz.
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["[-359, 359]"] = "[-359, 359]"
    
    #Parametrenin arayüzdeki başlığını ayarlamamızı sağlar.
    class Config:
        title = "Angle"

#burda da seçilen execuotra göre paket kaç tane input alacaksa alt alta yazılır.
class DirectionEstimationExecutorInputs(Inputs):
    inputImage: InputImage


class DirectionEstimationExecutorConfigs(Configs):
    degree: Degree
    drawBBox: KeepSideBBox

#paketimizin kaç tane outputu olacağını burada belirtiriz. birden fazla varsa alt alta yazarız.
#seçilen executorlara göre paketin outputları değişir.
class DirectionEstimationExecutorOutputs(Outputs):
    outputImage: OutputImage

#request olarak yani paketimize bir istek geldiğinde bu istekleri input ya da config olarak alırız.
class DirectionEstimationExecutorRequest(Request):
    inputs: Optional[DirectionEstimationExecutorInputs]
    configs: PDirectionEstimationExecutorConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class DirectionEstimationExecutorResponse(Response):
    outputs: DirectionEstimationExecutorOutputs

#oluşturacağımız executorun requestini ve responsunu burada belirtiriz.
class DirectionEstimationExecutorExecutor(Config):
    name: Literal["Package"] = "Package"
    value: Union[DirectionEstimationExecutorRequest, DirectionEstimationExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Package"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }

#paketin içerisinde kaç tane executor olacağının bilgisi burada girilir
class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[DirectionEstimationExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    # eğer birden fazla executor varsa ve bunlardan biri seçilecekse Config olarak json_schema_extra içerisinde target value olarak bilrtilir.
    class Config:
        title = "Task"
        json_schema_extra = {
            "target": "value"
        }


class PackageConfigs(Configs):
    executor: ConfigExecutor

#paketin tipi ne olacak component mi kapsül mü widgets mı burada belirtilir.
class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DirectionEstimation"] = "DirectionEstimation"
