from inference import InferencePipeline
import cv2

#Trata os resultados
def my_sink(result, video_frame):
    if result.get("output_image"):
        cv2.imshow("Imagem com detecções", result["output_image"].numpy_image)
        cv2.waitKey(1)

    motocicletas = []
    for p in result["predictions"]:
        if isinstance(p, dict):
            if p.get("class_name", "").lower() == "motocicleta":
                motocicletas.append(p)
        elif isinstance(p, tuple):
            if len(p) > 0 and str(p[0]).lower() == "motocicleta":
                motocicletas.append(p)

    print(f"Motocicletas detectadas: {len(motocicletas)}")


# Câmera/webcam
def p_camera(api_key, workspace_name, workflow_id, camera_id=0, max_fps=15):
    pipeline = InferencePipeline.init_with_workflow(
        api_key=api_key,
        workspace_name=workspace_name,
        workflow_id=workflow_id,
        video_reference=camera_id,
        max_fps=max_fps,
        on_prediction=my_sink
    )
    pipeline.start()
    pipeline.join()


# Vídeo local
def p_local(api_key, workspace_name, workflow_id, video_path, max_fps=15):
    pipeline = InferencePipeline.init_with_workflow(
        api_key=api_key,
        workspace_name=workspace_name,
        workflow_id=workflow_id,
        video_reference=video_path,
        max_fps=max_fps,
        on_prediction=my_sink
    )
    pipeline.start()
    pipeline.join()


# Configuração da API 
api_key = "secret"
workspace_name = "safeyard"
workflow_id = "detect-count-and-visualize-3"


# Video Local
# video_local = "videos/exemplo.mp4"
# p_local(api_key, workspace_name, workflow_id, video_local)

# Camera
p_camera(api_key, workspace_name, workflow_id, camera_id=0)