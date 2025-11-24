using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class APIClient : MonoBehaviour
{
    public string endpoint = "http://127.0.0.1:8000/upload-photos";

    public IEnumerator SendPhotos(List<Texture2D> photos)
    {
        WWWForm form = new WWWForm();

        for (int i = 0; i < photos.Count; i++)
        {
            byte[] imageBytes = photos[i].EncodeToPNG();
            form.AddBinaryData("files", imageBytes, $"photo_{i}.png", "image/png");
        }

        UnityWebRequest www = UnityWebRequest.Post(endpoint, form);
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success)
            Debug.Log("Upload successful: " + www.downloadHandler.text);
        else
            Debug.Log("Upload failed: " + www.error);
    }
}