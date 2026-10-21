//! Typestate makes a transition illegal at compile time.
//!
//! ```
//! use reas_typestate::Job;
//! let completed = Job::new(1).start().complete();
//! assert_eq!(completed.id(), 1);
//! ```
//!
//! ```compile_fail
//! use reas_typestate::Job;
//! let _invalid = Job::new(1).complete();
//! ```

use std::marker::PhantomData;
pub struct Pending;
pub struct Running;
pub struct Completed;
pub struct Job<State> { id: u64, state: PhantomData<State> }
impl Job<Pending> {
    pub fn new(id: u64) -> Self { Self { id, state: PhantomData } }
    pub fn start(self) -> Job<Running> { Job { id: self.id, state: PhantomData } }
}
impl Job<Running> {
    pub fn complete(self) -> Job<Completed> { Job { id: self.id, state: PhantomData } }
}
impl<State> Job<State> { pub fn id(&self) -> u64 { self.id } }

#[cfg(test)]
mod tests {
    use super::Job;
    #[test]
    fn a_running_job_can_complete() { assert_eq!(Job::new(123).start().complete().id(), 123); }
}
