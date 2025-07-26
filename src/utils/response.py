
from sdks.novavision.src.helper.package import PackageHelper
from components.DirectionEstimation.src.models.PackageModel import PackageModel, PackageConfigs, ConfigExecutor, DirectionEstimationExecutorOutputs, DirectionEstimationExecutorResponse, DirectionEstimationExecutor, OutputImage


def build_response(context):
    outputImage = OutputImage(value=context.image)
    directionEstimationOutputs = DirectionEstimationExecutorOutputs(outputImage=outputImage)
    directionEstimationResponse = DirectionEstimationExecutorResponse(outputs=directionEstimationOutputs)
    directionEstimationExecutor = DirectionEstimationExecutor(value=directionEstimationResponse)
    executor = ConfigExecutor(value=directionEstimationExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel