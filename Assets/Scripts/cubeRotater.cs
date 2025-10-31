using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO; // for reading json


public class cubeRotator : MonoBehaviour // from unity's mb class
{
    private class Moves
    {
        public string[] moves;
    }

    public Transform upPivot;
    public Transform downPivot;
    public Transform leftPivot;
    public Transform rightPivot;
    public Transform frontPivot;
    public Transform backPivot;

    private string[] moves; // will be given from backend/json file
    private List<Transform> allCubelets = new List<Transform>();

    void readMoves()
    {
        string path = "FIX: CHANGE TO ACTUAL PATHNAME"; // should come from json

        if (File.Exists(path))
        {
            string movesStr = File.ReadAllText(path);
            Moves moveList = JsonUtility.FromJson<Moves>(movesStr);
            moves = moveList.moves;
        }
        else
        {
            Debug.LogError("No file found in readMoves function\n");
            // may need to write/rewrite moves string here?
        }
    }

    IEnumerator executeMoves()
    {
        for (int i = 0; i < moves.Length; ++i)
        {
            Debug.Log("Executing rotation: " + moves[i] + '\n');
            yield return new WaitForSeconds(2f);
        }
    }

    void Start()
    {
        // save cubelets under parent (cube) and put into list
        for (int i = 0; i < transform.childCount; ++i)
        {
            Transform obj = transform.GetChild(i);
            if (!obj.name.Contains("Pivot")) // is cubelet
            {
                allCubelets.Add(obj);
            }
        }

        readMoves();
        StartCoroutine(executeMoves());
        
        return;
    }
}

