using NUnit.Framework;
using UnityEngine;

public class CubeRotatorAllTests
{
    private CubeRotaterTestable rotator;
    private GameObject rotatorObject;

    private Transform up, down, left, right, front, back;

    [SetUp]
    public void Setup()
    {
        rotatorObject = new GameObject("CubeRotatorTestObject");
        rotator = new CubeRotaterTestable();

        up = new GameObject("U").transform;
        down = new GameObject("D").transform;
        left = new GameObject("L").transform;
        right = new GameObject("R").transform;
        front = new GameObject("F").transform;
        back = new GameObject("B").transform;

        rotator.upPivot = up;
        rotator.downPivot = down;
        rotator.leftPivot = left;
        rotator.rightPivot = right;
        rotator.frontPivot = front;
        rotator.backPivot = back;
    }

    [TearDown]
    public void Teardown()
    {
        Object.DestroyImmediate(rotatorObject);
        Object.DestroyImmediate(up.gameObject);
        Object.DestroyImmediate(down.gameObject);
        Object.DestroyImmediate(left.gameObject);
        Object.DestroyImmediate(right.gameObject);
        Object.DestroyImmediate(front.gameObject);
        Object.DestroyImmediate(back.gameObject);
    }

//get axis testing 
    [Test]
    public void GetAxis_ReturnsUp_ForUMove()
    {
        Assert.AreEqual(Vector3.up, rotator.getAxis("U"));
    }

    [Test]
    public void GetAxis_ReturnsRight_ForRPrimeAndR2()
    {
        Assert.AreEqual(Vector3.right, rotator.getAxis("R'"));
        Assert.AreEqual(Vector3.right, rotator.getAxis("R2"));
    }

    [Test]
    public void GetAxis_ReturnsZero_ForInvalidMove()
    {
        Assert.AreEqual(Vector3.zero, rotator.getAxis("X"));
    }

//reverse testing
    [Test]
    public void GetReverse_PrimeMove_ReturnsNonPrime()
    {
        Assert.AreEqual("U", rotator.getReverse("U'"));
    }

    [Test]
    public void GetReverse_NormalMove_ReturnsPrimeVersion()
    {
        Assert.AreEqual("R'", rotator.getReverse("R"));
    }

    [Test]
    public void GetReverse_DoubleTurn_ReturnsSameMove()
    {
        Assert.AreEqual("F2", rotator.getReverse("F2"));
    }

 //pivot testing 
    [Test]
    public void GetPivot_ReturnsUpPivot()
    {
        Assert.AreEqual(up, rotator.getPivot("U"));
    }

    [Test]
    public void GetPivot_ReturnsFrontPivot()
    {
        Assert.AreEqual(front, rotator.getPivot("F"));
    }

    [Test]
    public void GetPivot_InvalidMove_ReturnsNull()
    {
        Assert.IsNull(rotator.getPivot("X"));
    }
}