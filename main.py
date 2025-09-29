from datetime import datetime, timedelta
from inference import InferencePipeline
import cv2
import oracledb

def save_db(qtd_motos):
    conn = oracledb.connect(
        user="",
        password="",
        dsn="oracle.fiap.com.br:1521/ORCL"
    )
    cursor = conn.cursor()
    agora = datetime.now()
    data = agora.date()
    hora = agora.strftime("%H:%M:%S")
    cursor.execute("""
        INSERT INTO TB_ECHO_MOTORCYCLE (QTD_MOTOS, HORA, DATA)
        VALUES (:qtd, :hora, :data)
    """, qtd=qtd_motos, hora=hora, data=data)
    conn.commit()
    cursor.close()
    conn.close()

motorcycle_ids = [set()]
last_db_save = [datetime.min]
def my_sink(result, video_frame):
    if result.get("output_image"):      
        cv2.imshow("Imagem com detecções", result["output_image"].numpy_image)
        cv2.waitKey(1)

    for p in result["predictions"]:
        print("Predição completa:", p)
        detection_id = None
        if isinstance(p, dict):
            if p.get("class_name", "").lower() == "motorcycle":
                detection_id = p.get("detection_id")
        elif isinstance(p, tuple):
            if len(p) > 5 and p[5].get("class_name", "").lower() == "motorcycle":
                detection_id = p[5].get("detection_id")
        if detection_id:
            motorcycle_ids[0].add(detection_id)

    agora = datetime.now()
    if (agora - last_db_save[0]).total_seconds() >= 0.5:
        qtd_motos = len(motorcycle_ids[0])
        print(f"Motocicletas únicas detectadas no período: {qtd_motos}")
        save_db(qtd_motos)
        motorcycle_ids[0].clear()
        last_db_save[0] = agora
    return []


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
api_key = "zl2QCx0S5KqmkOzxvjJs"
workspace_name = "safeyard"
workflow_id = "detect-count-and-visualize-3"


# Video Local
# video_local = "videos/exemplo.mp4"
# p_local(api_key, workspace_name, workflow_id, video_local)

# Camera
p_camera(api_key, workspace_name, workflow_id, camera_id=0)

