using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using System;

public class APIClient : MonoBehaviour
{
    public string endpoint = "http://127.0.0.1:8000/upload-photos";

    [Serializable]
    public class SolutionResponse
    {
        public string[] Solution;
        public string[] solution;
    }

    // Coroutine that sends photos and calls onSolutionReceived with the parsed array
    public IEnumerator SendPhotos(List<Texture2D> photos, Action<string[]> onSolutionReceived)
    {
        WWWForm form = new WWWForm();
        for (int i = 0; i < photos.Count; i++)
            form.AddBinaryData("files", photos[i].EncodeToPNG(), $"photo_{i}.png", "image/png");

        using (UnityWebRequest www = UnityWebRequest.Post(endpoint, form))
        {
            yield return www.SendWebRequest();

   
            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError($"Upload failed ({www.responseCode}): {www.error}\n{www.downloadHandler.text}");
                onSolutionReceived?.Invoke(null);
                yield break;
            }

            string text = www.downloadHandler.text;
            Debug.Log("Backend response: " + text);
            SolutionResponse response = JsonUtility.FromJson<SolutionResponse>(text);
            string[] solution = response.Solution ?? response.solution;
            if (solution == null || solution.Length == 0)
            {
                Debug.LogError("Backend response did not include a solution: " + text);
            }

            onSolutionReceived?.Invoke(solution);
        }
    }
}
