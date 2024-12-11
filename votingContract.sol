pragma solidity ^0.8.7;

contract VotingSystem {
    struct Candidate {
        string name;
        uint256 voteCount;
    }

    mapping(address => bool) public voters;
    Candidate[] public candidates;

    constructor(string[] memory _candidateNames) {
        for (uint256 i = 0; i < _candidateNames.length; i++) {
            candidates.push(Candidate({name: _candidateNames[i], voteCount: 0}));
        }
    }

    function vote(uint256 _candidateIndex) public {
        require(!voters[msg.sender], "Already voted");
        require(_candidateIndex < candidates.length, "Invalid candidate index");

        voters[msg.sender] = true;
        candidates[_candidateIndex].voteCount += 1;
    }

    function getCandidateCount() public view returns (uint256) {
        return candidates.length;
    }

    function getCandidate(uint256 _candidateIndex) public view returns (string memory, uint256) {
        require(_candidateIndex < candidates.length, "Invalid candidate index");

        return (candidates[_candidateIndex].name, candidates[_candidateIndex].voteCount);
    }
}