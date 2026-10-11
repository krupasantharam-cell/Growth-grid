// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title GrowthGridBadges
 * @dev Verifiable, Soulbound STEM Skill-Credential Badges on Polygon Testnet.
 * PRIVACY GUARANTEE: Never stores personal names, emails, or personal data on-chain.
 * Only cryptographic hashes (SHA-256) of learner credentials and mastery proofs are stored.
 */
contract GrowthGridBadges {
    address public immutable owner;

    struct CredentialRecord {
        bytes32 badgeHash;       // Deterministic cryptographic hash of the credential
        bytes32 studentHash;     // Pseudonymous student hash (SHA-256(student_id + salt))
        uint256 topicId;         // STEM Topic Identifier
        uint256 masteryScore;    // Mastery score percentage achieved (80-100)
        uint256 issuedAt;        // Block timestamp
        string metadataUri;      // IPFS/Arweave or HTTPS metadata pointer
        address issuer;          // Growth Grid authorized issuing authority
    }

    // Mapping from badgeHash to CredentialRecord
    mapping(bytes32 => CredentialRecord) public credentials;
    // Mapping from studentHash to array of badgeHashes
    mapping(bytes32 => bytes32[]) private studentBadges;

    event BadgeIssued(
        bytes32 indexed badgeHash,
        bytes32 indexed studentHash,
        uint256 indexed topicId,
        uint256 masteryScore,
        uint256 issuedAt
    );

    event BadgeRevoked(bytes32 indexed badgeHash);

    modifier onlyOwner() {
        require(msg.sender == owner, "GrowthGrid: caller is not authorized");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    /**
     * @notice Issues a verifiable credential badge.
     * @param badgeHash SHA-256 hash of badge payload
     * @param studentHash Pseudonymous student hash
     * @param topicId Topic identifier
     * @param masteryScore Mastery percentage (>= 80)
     * @param metadataUri URI pointing to public badge schema metadata
     */
    function issueBadge(
        bytes32 badgeHash,
        bytes32 studentHash,
        uint256 topicId,
        uint256 masteryScore,
        string calldata metadataUri
    ) external onlyOwner {
        require(credentials[badgeHash].issuedAt == 0, "GrowthGrid: Badge already issued");
        require(masteryScore >= 80, "GrowthGrid: Mastery gate requires >= 80%");

        credentials[badgeHash] = CredentialRecord({
            badgeHash: badgeHash,
            studentHash: studentHash,
            topicId: topicId,
            masteryScore: masteryScore,
            issuedAt: block.timestamp,
            metadataUri: metadataUri,
            issuer: msg.sender
        });

        studentBadges[studentHash].push(badgeHash);

        emit BadgeIssued(badgeHash, studentHash, topicId, masteryScore, block.timestamp);
    }

    /**
     * @notice Verifies a credential by its badge hash.
     */
    function verifyBadge(bytes32 badgeHash)
        external
        view
        returns (
            bool isValid,
            bytes32 studentHash,
            uint256 topicId,
            uint256 masteryScore,
            uint256 issuedAt,
            address issuer
        )
    {
        CredentialRecord memory rec = credentials[badgeHash];
        if (rec.issuedAt == 0) {
            return (false, bytes32(0), 0, 0, 0, address(0));
        }
        return (true, rec.studentHash, rec.topicId, rec.masteryScore, rec.issuedAt, rec.issuer);
    }

    /**
     * @notice Returns all badge hashes belonging to an anonymous student hash.
     */
    function getStudentBadges(bytes32 studentHash) external view returns (bytes32[] memory) {
        return studentBadges[studentHash];
    }
}
