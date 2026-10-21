//! This example keeps the domain, application port, and concrete adapter discoverable.

pub mod domain {
    #[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
    pub struct TeamId(pub u32);

    #[derive(Debug, Clone, PartialEq, Eq)]
    pub struct Team {
        pub id: TeamId,
        pub name: String,
    }
}

pub mod application {
    use crate::domain::{Team, TeamId};

    pub trait TeamRepository {
        fn find(&self, id: TeamId) -> Option<Team>;
    }

    pub struct FindTeam<R> {
        repository: R,
    }

    impl<R: TeamRepository> FindTeam<R> {
        pub fn new(repository: R) -> Self {
            Self { repository }
        }

        pub fn execute(&self, id: TeamId) -> Option<Team> {
            self.repository.find(id)
        }
    }
}

pub mod adapters {
    use std::collections::HashMap;

    use crate::application::TeamRepository;
    use crate::domain::{Team, TeamId};

    pub struct InMemoryTeamRepository {
        teams: HashMap<TeamId, Team>,
    }

    impl InMemoryTeamRepository {
        pub fn new(teams: impl IntoIterator<Item = Team>) -> Self {
            let teams = teams.into_iter().map(|team| (team.id, team)).collect();
            Self { teams }
        }
    }

    impl TeamRepository for InMemoryTeamRepository {
        fn find(&self, id: TeamId) -> Option<Team> {
            self.teams.get(&id).cloned()
        }
    }
}

#[cfg(test)]
mod tests {
    use crate::adapters::InMemoryTeamRepository;
    use crate::application::FindTeam;
    use crate::domain::{Team, TeamId};

    #[test]
    fn the_adapter_is_wired_explicitly() {
        let repository = InMemoryTeamRepository::new([Team {
            id: TeamId(3),
            name: "Warriors".to_owned(),
        }]);
        let find_team = FindTeam::new(repository);
        assert_eq!(find_team.execute(TeamId(3)).unwrap().name, "Warriors");
        assert!(find_team.execute(TeamId(9)).is_none());
    }
}
