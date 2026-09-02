using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using UnityEngine;
using UnityEngine.Networking;
using Debug = UnityEngine.Debug;

public class BackendLauncher : MonoBehaviour
{
    private const string HealthUrl = "http://127.0.0.1:8000/docs";
    private static BackendLauncher instance;
    private Process backendProcess;

    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
    private static void CreateLauncher()
    {
        if (instance != null)
            return;

        GameObject launcherObject = new GameObject("BackendLauncher");
        instance = launcherObject.AddComponent<BackendLauncher>();
        DontDestroyOnLoad(launcherObject);
    }

    private void Start()
    {
        StartCoroutine(StartBackendIfNeeded());
    }

    private IEnumerator StartBackendIfNeeded()
    {
        yield return CheckBackendRunning(isRunning =>
        {
            if (isRunning)
            {
                Debug.Log("Backend is already running.");
                return;
            }

            LaunchBackend();
        });
    }

    private IEnumerator CheckBackendRunning(System.Action<bool> callback)
    {
        using (UnityWebRequest request = UnityWebRequest.Get(HealthUrl))
        {
            request.timeout = 2;
            yield return request.SendWebRequest();
            callback(request.result == UnityWebRequest.Result.Success);
        }
    }

    private void LaunchBackend()
    {
        string scriptPath = FindBackendScript();
        if (string.IsNullOrEmpty(scriptPath))
        {
            Debug.LogWarning("Backend start script was not found. Start the backend manually before submitting photos.");
            return;
        }

        try
        {
            ProcessStartInfo startInfo = CreateStartInfo(scriptPath);
            backendProcess = Process.Start(startInfo);
            Debug.Log("Started backend from: " + scriptPath);
        }
        catch (System.Exception ex)
        {
            Debug.LogError("Could not start backend: " + ex.Message);
        }
    }

    private string FindBackendScript()
    {
        string scriptName =
#if UNITY_STANDALONE_WIN
            "start_backend.bat";
#else
            "start_backend.command";
#endif

        foreach (string directory in GetSearchDirectories())
        {
            string path = Path.Combine(directory, scriptName);
            if (File.Exists(path))
                return path;
        }

        return null;
    }

    private string[] GetSearchDirectories()
    {
        List<string> directories = new List<string>();

        AddDirectory(directories, Directory.GetCurrentDirectory());
        AddDirectory(directories, Application.dataPath);

        DirectoryInfo current = Directory.GetParent(Application.dataPath);
        while (current != null)
        {
            AddDirectory(directories, current.FullName);
            current = current.Parent;
        }

        return directories.ToArray();
    }

    private void AddDirectory(List<string> directories, string path)
    {
        if (!string.IsNullOrEmpty(path) && !directories.Contains(path))
            directories.Add(path);
    }

    private ProcessStartInfo CreateStartInfo(string scriptPath)
    {
#if UNITY_STANDALONE_WIN
        return new ProcessStartInfo
        {
            FileName = "cmd.exe",
            Arguments = "/c \"" + scriptPath + "\"",
            WorkingDirectory = Path.GetDirectoryName(scriptPath),
            UseShellExecute = false,
            CreateNoWindow = true
        };
#else
        return new ProcessStartInfo
        {
            FileName = "/bin/bash",
            Arguments = "\"" + scriptPath + "\"",
            WorkingDirectory = Path.GetDirectoryName(scriptPath),
            UseShellExecute = false,
            CreateNoWindow = true
        };
#endif
    }

    private void OnApplicationQuit()
    {
        try
        {
            if (backendProcess == null || backendProcess.HasExited)
                return;

#if UNITY_STANDALONE_WIN
            Process.Start(new ProcessStartInfo
            {
                FileName = "taskkill",
                Arguments = "/PID " + backendProcess.Id + " /T /F",
                CreateNoWindow = true,
                UseShellExecute = false
            });
#else
            backendProcess.Kill();
#endif
            backendProcess.Dispose();
        }
        catch (System.Exception ex)
        {
            Debug.LogWarning("Backend shutdown skipped: " + ex.Message);
        }
    }
}
