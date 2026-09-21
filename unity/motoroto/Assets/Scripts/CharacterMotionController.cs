using UnityEngine;

public class CharacterMotionController : MonoBehaviour
{
    private Animator animator;

    private Transform leftLowerArm;
    private Transform rightLowerArm;

    private Transform leftLowerLeg;
    private Transform rightLowerLeg;

    private Transform spine;
    private Transform chest;
    private Transform neck;
    private Transform head;

    private Quaternion leftArmStart;
    private Quaternion rightArmStart;

    private Quaternion leftLegStart;
    private Quaternion rightLegStart;

    private Quaternion spineStart;
    private Quaternion chestStart;
    private Quaternion neckStart;
    private Quaternion headStart;

    void Start()
    {
        animator = GetComponent<Animator>();

        leftLowerArm =
            animator.GetBoneTransform(HumanBodyBones.LeftLowerArm);

        rightLowerArm =
            animator.GetBoneTransform(HumanBodyBones.RightLowerArm);

        leftLowerLeg =
            animator.GetBoneTransform(HumanBodyBones.LeftLowerLeg);

        rightLowerLeg =
            animator.GetBoneTransform(HumanBodyBones.RightLowerLeg);

        spine =
            animator.GetBoneTransform(HumanBodyBones.Spine);

        chest =
            animator.GetBoneTransform(HumanBodyBones.Chest);

        neck =
            animator.GetBoneTransform(HumanBodyBones.Neck);

        head =
            animator.GetBoneTransform(HumanBodyBones.Head);

        leftArmStart = leftLowerArm.localRotation;
        rightArmStart = rightLowerArm.localRotation;

        leftLegStart = leftLowerLeg.localRotation;
        rightLegStart = rightLowerLeg.localRotation;

        if (spine != null)
            spineStart = spine.localRotation;

        if (chest != null)
            chestStart = chest.localRotation;

        if (neck != null)
            neckStart = neck.localRotation;

        if (head != null)
            headStart = head.localRotation;

        Debug.Log("MotionLens full body controller ready.");
    }

    public void UpdateMotion(MotionData motion)
    {
        if (motion == null || motion.pose == null)
            return;

        UpdateArms(motion);
        UpdateLegs(motion);
        UpdateTorso(motion);
        UpdateHead(motion);
    }

    // =====================================================
    // ARMS
    // =====================================================

    private void UpdateArms(MotionData motion)
    {
        float leftBend =
            Mathf.InverseLerp(180f, 30f, motion.pose.left_elbow);

        float rightBend =
            Mathf.InverseLerp(180f, 30f, motion.pose.right_elbow);

        float leftRotation =
            Mathf.Lerp(0f, -70f, leftBend);

        float rightRotation =
            Mathf.Lerp(0f, 70f, rightBend);

        leftLowerArm.localRotation =
            leftArmStart *
            Quaternion.Euler(leftRotation, 0f, 0f);

        rightLowerArm.localRotation =
            rightArmStart *
            Quaternion.Euler(rightRotation, 0f, 0f);
    }

    // =====================================================
    // LEGS
    // =====================================================

    private void UpdateLegs(MotionData motion)
    {
        float leftBend =
            Mathf.InverseLerp(180f, 30f, motion.pose.left_knee);

        float rightBend =
            Mathf.InverseLerp(180f, 30f, motion.pose.right_knee);

        float leftRotation =
            Mathf.Lerp(0f, -90f, leftBend);

        float rightRotation =
            Mathf.Lerp(0f, 90f, rightBend);

        leftLowerLeg.localRotation =
            leftLegStart *
            Quaternion.Euler(leftRotation, 0f, 0f);

        rightLowerLeg.localRotation =
            rightLegStart *
            Quaternion.Euler(rightRotation, 0f, 0f);
    }

    // =====================================================
    // TORSO
    // =====================================================

    private void UpdateTorso(MotionData motion)
    {
        if (motion.landmarks == null)
            return;

        Landmark ls = motion.landmarks.left_shoulder;
        Landmark rs = motion.landmarks.right_shoulder;
        Landmark lh = motion.landmarks.left_hip;
        Landmark rh = motion.landmarks.right_hip;

        if (ls.visibility < 0.5f ||
            rs.visibility < 0.5f ||
            lh.visibility < 0.5f ||
            rh.visibility < 0.5f)
        {
            return;
        }

        Vector3 shoulderCenter =
            (ToUnityPosition(ls) +
             ToUnityPosition(rs)) * 0.5f;

        Vector3 hipCenter =
            (ToUnityPosition(lh) +
             ToUnityPosition(rh)) * 0.5f;

        Vector3 torsoDirection =
            (shoulderCenter - hipCenter).normalized;

        float leanX =
            Mathf.Clamp(
                Mathf.Atan2(
                    torsoDirection.z,
                    torsoDirection.y
                ) * Mathf.Rad2Deg,
                -25f,
                25f
            );

        float leanZ =
            Mathf.Clamp(
                Mathf.Atan2(
                    torsoDirection.x,
                    torsoDirection.y
                ) * Mathf.Rad2Deg,
                -25f,
                25f
            );

        Quaternion torsoRotation =
            Quaternion.Euler(
                leanX * 0.5f,
                0f,
                -leanZ * 0.5f
            );

        if (spine != null)
            spine.localRotation =
                spineStart * torsoRotation;

        if (chest != null)
            chest.localRotation =
                chestStart * torsoRotation;
    }

    // =====================================================
    // HEAD
    // =====================================================

    private void UpdateHead(MotionData motion)
    {
        if (motion.landmarks == null ||
            motion.landmarks.nose == null)
            return;

        Landmark nose = motion.landmarks.nose;
        Landmark ls = motion.landmarks.left_shoulder;
        Landmark rs = motion.landmarks.right_shoulder;

        if (nose.visibility < 0.5f ||
            ls.visibility < 0.5f ||
            rs.visibility < 0.5f)
        {
            return;
        }

        Vector3 nosePos =
            ToUnityPosition(nose);

        Vector3 shoulderCenter =
            (ToUnityPosition(ls) +
             ToUnityPosition(rs)) * 0.5f;

        Vector3 direction =
            (nosePos - shoulderCenter).normalized;

        float pitch =
            Mathf.Clamp(
                direction.y * 35f,
                -20f,
                20f
            );

        float yaw =
            Mathf.Clamp(
                direction.x * 35f,
                -20f,
                20f
            );

        Quaternion headRotation =
            Quaternion.Euler(
                -pitch,
                yaw,
                0f
            );

        if (neck != null)
            neck.localRotation =
                neckStart * headRotation;

        if (head != null)
            head.localRotation =
                headStart * headRotation;
    }

    // =====================================================
    // MEDIAPIPE → UNITY
    // =====================================================

    private Vector3 ToUnityPosition(Landmark landmark)
    {
        return new Vector3(
            -landmark.x,
            -landmark.y,
            landmark.z
        );
    }
}