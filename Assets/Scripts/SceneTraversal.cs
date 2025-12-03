using UnityEngine;
using UnityEngine.SceneManagement;

public class SceneTraversal : MonoBehaviour
{
    public void TransitionScene(string scene)
    {
        SceneManager.LoadScene(scene);
    }

    public void QuitGame()
    {
        Application.Quit();
    }
}