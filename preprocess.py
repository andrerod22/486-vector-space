
    physical_page& operator=(const physical_page&) = delete;
    physical_page(const physical_page&) = delete;
    physical_page(physical_page&& RHS) noexcept:job_requesters(move(RHS.job_requesters)){ };
    physical_page& operator-(physical_page&& RHS) noexcept{
        job_requesters = move(RHS.job_requesters);
        return *this;
    }

