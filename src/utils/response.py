
from sdks.novavision.src.helper.package import PackageHelper
from components.DirectionEstimation.src.models.PackageModel import PackageModel, PackageConfigs, ConfigExecutor, DirectionEstimationOutputs, DirectionEstimationResponse, DirectionEstimationExecutor, OutputImage


def build_response(context):    
    outputImage = OutputImage(value=context.image)
    DirectionEstimationOutputs = DirectionEstimationOutputs(outputImage=outputImage)
    DirectionEstimationResponse = DirectionEstimationResponse(outputs=Outputs)
    DirectionEstimationExecutor = DirectionEstimationExecutor(value=packageResponse)
    executor = ConfigExecutor(value=DirectionEstimationExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel