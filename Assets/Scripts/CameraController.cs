using UnityEngine;

public class CameraController : MonoBehaviour
{
    public Camera cam;

    private void Awake()
    {
        if (cam == null)
        {
            cam = Camera.main;
        }

        if (cam == null)
        {
            Debug.LogError("CameraController: no Camera assigned and Camera.main is null");
        }
    }

    public Texture2D CapturePhoto()
    {
        if (cam == null)
        {
            Debug.LogError("CapturePhoto: cam is null");
            return null;
        }

        RenderTexture rt = new RenderTexture(Screen.width, Screen.height, 24);
        cam.targetTexture = rt;
        cam.Render();
        RenderTexture.active = rt;

        Texture2D photo = new Texture2D(rt.width, rt.height, TextureFormat.RGB24, false);
        photo.ReadPixels(new Rect(0, 0, rt.width, rt.height), 0, 0);
        photo.Apply();

        cam.targetTexture = null;
        RenderTexture.active = null;
        Destroy(rt);

        return photo;
    }
}